import { By, Builder, Browser } from "selenium-webdriver";
import dotenv from "dotenv";

dotenv.config();

// the buyer approves an order using the PayPal UI
export const approveOrder = async (approveLink) => {
  let driver;
  try {
    driver = await new Builder().forBrowser(Browser.CHROME).build();
    // visit approveLink URL
    await driver.get(approveLink);

    await driver.sleep(1000); // Delay needed

    // fill in the email
    let emailInput = await driver.findElement(By.id("email"));
    await emailInput.sendKeys(process.env.PAYPAL_EMAIL);

    // click Next button
    let nextButton = await driver.findElement(By.id("btnNext"));
    await nextButton.click();
    await driver.sleep(2500); // Delay needed

    // fill in the password
    const passwordInput = await driver.findElement(By.id("password"));
    await passwordInput.sendKeys(process.env.PAYPAL_PASSWORD);

    // Click login button
    let btnLogin = await driver.findElement(By.id("btnLogin"));
    await btnLogin.click();

    await driver.sleep(500); // Delay needed

    // Click submit button
    let submitBtn = await driver.findElement(By.id("payment-submit-btn"));
    await submitBtn.click();

    await driver.sleep(3500); // Delay needed

    await driver.manage().setTimeouts({ implicit: 500 });
  } catch (e) {
    console.log(e);
  } finally {
    // close the browser
    await driver.quit();
  }
};
