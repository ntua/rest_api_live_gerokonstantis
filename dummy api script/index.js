import axios from "axios";

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function printInfo(res) {
  console.log(
    `${requestCounter++}. ${res.request.method} ${
      res.config.url
    } - STATUS CODE:`,
    res.status,
    "\x1b[32m✔\x1b[0m"
  );
}

function printErrorInfo(error) {
  console.log(
    `${requestCounter++}. ${error.request.method} ${error.config.url} :`,
    error.response.data.message,
    "\x1b[31m✕\x1b[0m"
  );
}

const currentUseCase = "1";

const baseURL = `http://localhost:3003/proxy/https_dummyjson_com/${currentUseCase}`;

var requestCounter = 1;

console.log("USE CASE 1 : Posts");

// List all posts
try {
  let res = await axios.get(`${baseURL}/posts`);
  printInfo(res);
} catch (error) {
  printErrorInfo(res);
}

// Get info about a post
try {
  let res = await axios.get(`${baseURL}/posts/17`);
  printInfo(res);
} catch (error) {
  printErrorInfo(res);
}

// Get posts with tag=life
try {
  let res = await axios.get(`${baseURL}/posts/tag/love`);
  printInfo(res);
} catch (error) {
  printErrorInfo(res);
}

// Get posts of user 5
try {
  let res = await axios.get(`${baseURL}/posts/user/5`);
  printInfo(res);
} catch (error) {
  printErrorInfo(res);
}

// Update a post
try {
  let res = await axios.put(`${baseURL}/posts/17`, {
    title: "Dummy title updated",
  });
  printInfo(res);
} catch (error) {
  printErrorInfo(res);
}

// Delete the post
try {
  let res = await axios.delete(`${baseURL}/posts/17`);
  printInfo(res);
} catch (error) {
  printErrorInfo(res);
}
