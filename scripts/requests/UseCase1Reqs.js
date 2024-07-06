import axios from "axios";
import logSymbols from "log-symbols";
import {
  createProductReqBody,
  updateProductReqBody,
  createOrderReqBody,
  updateOrderReqBody,
  captureAuthorizedPaymentReqBody,
  addTrackingInfoReqBody,
  updateTrackingInfoReqBody,
} from "./requestBodies/UseCase1.js";
import { approveOrder } from "./selenium/seleniumFunctions.js";

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
// handling tracking information requires the initial paypal auth token
//(owned by a random merchant, not the one associated with the business sandbox account)
const authHeader = `Bearer ${process.env.PAYPAL_INITIAL_AUTH_TOKEN}`;
const headers = {
  headers: {
    Authorization: authHeader,
  },
};

var requestCounter = 1;

export const useCase1Requests = async () => {
  // Use Case 1 : Create Product - New Order - Payment - Tracking
  console.log("USE CASE 1 : Create Product - New Order - Payment - Tracking");
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

  // Show details about the product
  try {
    let res = await axios.get(
      `${baseURL}/v1/catalogs/products/${productID}`,
      headers
    );
    printInfo(res);
  } catch (error) {
    printErrorInfo(error);
  }

  await sleep(1000);

  // Update product
  try {
    let res = await axios.patch(
      `${baseURL}/v1/catalogs/products/${productID}`,
      updateProductReqBody(),
      headers
    );
    printInfo(res);
  } catch (error) {
    printErrorInfo(error);
  }

  await sleep(1000);

  // Create order for this product
  let orderID = "";
  let approveLink = "";
  try {
    let res = await axios.post(
      `${baseURL}/v2/checkout/orders`,
      createOrderReqBody(),
      headers
    );
    printInfo(res);
    orderID = res.data.id;
    approveLink = res.data.links.find((link) => link.rel === "approve").href;
  } catch (error) {
    printErrorInfo(error);
  }

  await sleep(1000);

  // Update order
  try {
    let res = await axios.patch(
      `${baseURL}/v2/checkout/orders/${orderID}`,
      updateOrderReqBody(),
      headers
    );
    printInfo(res);
  } catch (error) {
    printErrorInfo(error);
  }

  await sleep(1000);

  // show order details
  try {
    let res = await axios.get(
      `${baseURL}/v2/checkout/orders/${orderID}`,
      headers
    );
    printInfo(res);
  } catch (error) {
    printErrorInfo(error);
  }

  await approveOrder(approveLink);
  console.log(`${requestCounter++}. Order approved`, logSymbols.success);

  await sleep(1000);

  // authorize payment for order
  let authorizationID = "";
  try {
    let res = await axios.post(
      `${baseURL}/v2/checkout/orders/${orderID}/authorize`,
      {},
      headers
    );
    authorizationID = res.data.purchase_units[0].payments.authorizations[0].id;
    printInfo(res);
  } catch (error) {
    printErrorInfo(error);
  }

  await sleep(1000);

  // show details for authorized payment
  try {
    let res = await axios.get(
      `${baseURL}/v2/payments/authorizations/${authorizationID}`,
      headers
    );
    printInfo(res);
  } catch (error) {
    printErrorInfo(error);
  }

  await sleep(1000);

  // capture authorized payment
  let captureID = "";
  try {
    let res = await axios.post(
      `${baseURL}/v2/payments/authorizations/${authorizationID}/capture`,
      captureAuthorizedPaymentReqBody(Date.now()),
      headers
    );
    captureID = res.data.id;
    printInfo(res);
  } catch (error) {
    printErrorInfo(error);
  }

  await sleep(1000);

  // show captured payment details
  try {
    let res = await axios.get(
      `${baseURL}/v2/payments/captures/${captureID}`,
      headers
    );
    printInfo(res);
  } catch (error) {
    printErrorInfo(error);
  }

  await sleep(1000);

  // add tracking information
  let trackingID = "";
  const trackingNumber = Date.now();
  try {
    let res = await axios.post(
      `${baseURL}/v1/shipping/trackers-batch`,
      addTrackingInfoReqBody(captureID, trackingNumber),
      headers
    );
    trackingID =
      res.data.tracker_identifiers[0].transaction_id +
      "-" +
      `${trackingNumber}`;
    printInfo(res);
  } catch (error) {
    printErrorInfo(error);
  }

  await sleep(1000);

  // show tracking information
  try {
    let res = await axios.get(
      `${baseURL}/v1/shipping/trackers/${trackingID}`,
      headers
    );
    printInfo(res);
  } catch (error) {
    printErrorInfo(error);
  }

  await sleep(1000);

  // update tracking information (carrier)
  try {
    let res = await axios.put(
      `${baseURL}/v1/shipping/trackers/${trackingID}`,
      updateTrackingInfoReqBody(captureID, trackingNumber),
      headers
    );
    printInfo(res);
  } catch (error) {
    printErrorInfo(error);
  }
};
