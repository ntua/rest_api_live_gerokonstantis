import axios from "axios";
import logSymbols from "log-symbols";
import { approveOrder } from "./selenium/seleniumFunctions.js";
import {
  createProductReqBody,
  createOrderReqBody,
  refundCapturedPaymentReqBody,
} from "./requestBodies/UseCase1c.js";

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function printInfo(res) {
  console.log(
    `${requestCounter++}. ${res.request.method} ${
      res.config.url
    } - STATUS CODE:`,
    res.status,
    logSymbols.success
  );
}

function printErrorInfo(error) {
  console.log(
    `${requestCounter++}. ${error.request.method} ${error.config.url} :`,
    error.response.data.message,
    logSymbols.error
  );
}

const baseURL = `http://localhost:${process.env.MIM_PORT}/proxy/https_api-m_sandbox_paypal_com`;
const authHeader = `Bearer ${process.env.PAYPAL_AUTH_TOKEN}`;
const headers = {
  headers: {
    Authorization: authHeader,
  },
};

var requestCounter = 1;

export const useCase1cRequests = async () => {
  // Use Case 1c : Make Order - Pay - Refund
  console.log("USE CASE 1c : Make Order - Pay - Refund");
  // Create Product
  let productID = "";
  try {
    let res = await axios.post(
      `${baseURL}/v1/catalogs/products`,
      createProductReqBody(Date.now()),
      headers
    );
    printInfo(res);
    productID = res.data.id;
  } catch (error) {
    printErrorInfo(error);
  }

  await sleep(1000);

  // Show product details
  try {
    let res = await axios.get(
      `${baseURL}/v1/catalogs/products/${productID}`,
      headers
    );
    printInfo(res);
  } catch (error) {
    printErrorInfo(error);
  }

  // Create Order for this product
  let approveLink = "";
  let orderID = "";
  try {
    let res = await axios.post(
      `${baseURL}/v2/checkout/orders`,
      createOrderReqBody(),
      headers
    );
    printInfo(res);
    approveLink = res.data.links.find((link) => link.rel === "approve").href;
    orderID = res.data.id;
  } catch (error) {
    printErrorInfo(error);
  }

  await sleep(1000);

  // the buyer approves the order
  await approveOrder(approveLink);
  console.log(`${requestCounter++}. Order approved`, logSymbols.success);

  await sleep(1000);

  // Capture payment for order
  let captureID = "";
  try {
    let res = await axios.post(
      `${baseURL}/v2/checkout/orders/${orderID}/capture`,
      {},
      headers
    );
    printInfo(res);
    captureID = res.data.purchase_units[0].payments.captures[0].id;
  } catch (error) {
    printErrorInfo(error);
  }

  await sleep(1000);

  // Refund payment
  let refundID = "";
  try {
    let res = await axios.post(
      `${baseURL}/v2/payments/captures/${captureID}/refund`,
      refundCapturedPaymentReqBody(Date.now()),
      headers
    );
    printInfo(res);
    refundID = res.data.id;
  } catch (error) {
    printErrorInfo(error);
  }

  await sleep(1000);

  // Show refund details
  try {
    let res = await axios.get(
      `${baseURL}/v2/payments/refunds/${refundID}`,
      headers
    );
    printInfo(res);
    refundID = res.data.id;
  } catch (error) {
    printErrorInfo(error);
  }
};