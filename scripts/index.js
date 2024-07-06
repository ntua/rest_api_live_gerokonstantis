import axios from "axios";
import { approveOrder } from "./selenium/seleniumFunctions.js";
import { CreateProductReqBody } from "./requestBodies/Use Case 1c/CreateProduct.js";
import { createOrderReqBody } from "./requestBodies/Use Case 1c/CreateOrder.js";
import { refundCapturedPaymentReqBody } from "./requestBodies/Use Case 1c/RefundCapturedPayment.js";

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

const baseURL = `http://localhost:${process.env.MIM_PORT}/proxy/https_api-m_sandbox_paypal_com`;
const authHeader = `Bearer ${process.env.PAYPAL_AUTH_TOKEN}`;
const headers = {
  headers: {
    Authorization: authHeader,
  },
};

// Use Case 1c : Make Order - Pay - Refund
console.log("USE CASE 1c : Make Order - Pay - Refund");
// Create Product
let productID = "";
try {
  let res = await axios.post(
    `${baseURL}/v1/catalogs/products`,
    CreateProductReqBody,
    headers
  );
  console.log(
    "1. https://api-m.sandbox.paypal.com/v1/catalogs/products - STATUS CODE:",
    res.status
  );
  productID = res.data.id;
} catch (error) {
  console.log(
    "1. https://api-m.sandbox.paypal.com/v1/catalogs/products :",
    error.response.data.message
  );
}

await sleep(1000);

// Show product details
try {
  let res = await axios.get(
    `${baseURL}/v1/catalogs/products/${productID}`,
    headers
  );
  console.log(
    `2. https://api-m.sandbox.paypal.com/v1/catalogs/products/${productID} - STATUS CODE:`,
    res.status
  );
} catch (error) {
  console.log(
    `2. https://api-m.sandbox.paypal.com/v1/catalogs/products/${productID} :`,
    error.response.data.message
  );
}

// Create Order for this product
let approveLink = "";
let orderID = "";
try {
  let res = await axios.post(
    `${baseURL}/v2/checkout/orders`,
    createOrderReqBody,
    headers
  );
  console.log(
    `3. https://api-m.sandbox.paypal.com/v2/checkout/orders - STATUS CODE:`,
    res.status
  );
  approveLink = res.data.links.find((link) => link.rel === "approve").href;
  orderID = res.data.id;
} catch (error) {
  console.log(
    `3. https://api-m.sandbox.paypal.com/v2/checkout/orders :`,
    error.response.data.message
  );
}

await sleep(1000);

await approveOrder(approveLink);

await sleep(1000);

// Capture payment for order
let captureID = "";
try {
  let res = await axios.post(
    `${baseURL}/v2/checkout/orders/${orderID}/capture`,
    {},
    headers
  );
  console.log(
    `5. https://api-m.sandbox.paypal.com/v2/checkout/orders/${orderID}/capture - STATUS CODE:`,
    res.status
  );
  captureID = res.data.purchase_units[0].payments.captures[0].id;
} catch (error) {
  console.log(
    `5. https://api-m.sandbox.paypal.com/v2/checkout/orders/${orderID}/capture :`,
    error.response.data.message,
    error
  );
}

await sleep(1000);

// Refund payment
let refundID = "";
try {
  let res = await axios.post(
    `${baseURL}/v2/payments/captures/${captureID}/refund`,
    refundCapturedPaymentReqBody,
    headers
  );
  console.log(
    `6. https://api-m.sandbox.paypal.com/v2/payments/captures/${captureID}/refund - STATUS CODE:`,
    res.status
  );
  refundID = res.data.id;
} catch (error) {
  console.log(
    `6. https://api-m.sandbox.paypal.com/v2/payments/captures/${captureID}/refund :`,
    error.response.data.message,
    error
  );
}

await sleep(1000);

// Show refund details
try {
  let res = await axios.get(
    `${baseURL}/v2/payments/refunds/${refundID}`,
    headers
  );
  console.log(
    `7. https://api-m.sandbox.paypal.com/v2/payments/refunds/${refundID} - STATUS CODE:`,
    res.status
  );
  refundID = res.data.id;
} catch (error) {
  console.log(
    `7. https://api-m.sandbox.paypal.com/v2/payments/refunds/${refundID} :`,
    error.response.data.message,
    error
  );
}
