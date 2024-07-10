import { By, Builder, Browser, Key, until } from "selenium-webdriver";
import dotenv from "dotenv";
import path from "path";

dotenv.config();

// the buyer approves an order using the PayPal UI
export const approveOrder = async (approveLink) => {
  let driver;
  try {
    driver = await new Builder().forBrowser(Browser.CHROME).build();
    // Set the position and size of the browser window
    await driver
      .manage()
      .window()
      .setRect({ width: 600, height: 900, x: 120, y: 50 });
    // visit approveLink URL
    await driver.get(approveLink);

    await driver.sleep(1000); // Delay needed

    // fill in the email
    let emailInput = await driver.findElement(By.id("email"));
    await emailInput.sendKeys(process.env.PAYPAL_EMAIL);
    await driver.sleep(500); // Delay needed
    // click Next button
    let nextButton = await driver.findElement(By.id("btnNext"));
    await nextButton.click();
    await driver.sleep(2500); // Delay needed

    // fill in the password
    const passwordInput = await driver.findElement(By.id("password"));
    await passwordInput.sendKeys(process.env.PAYPAL_PASSWORD);
    await driver.sleep(500); // Delay needed
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

export const createDispute = async () => {
  let driver;
  try {
    driver = await new Builder().forBrowser(Browser.CHROME).build();

    // Set the position and size of the browser window
    await driver
      .manage()
      .window()
      .setRect({ width: 1200, height: 1000, x: 100, y: 50 });

    // visit PayPal activities page
    await driver.get(
      `https://www.sandbox.paypal.com/myaccount/activities/?free_text_search=&type=PAYMENT_SENT&status=&currency=&filter_id=&issuance_product_name=&asset_names=&asset_symbols=`
    );

    await driver.sleep(1000); // Delay needed

    // fill in the email
    let emailInput = await driver.findElement(By.id("email"));
    await emailInput.sendKeys(process.env.PAYPAL_EMAIL);
    await driver.sleep(500); // Delay needed
    // click Next button
    let nextButton = await driver.findElement(By.id("btnNext"));
    await nextButton.click();
    await driver.sleep(2500); // Delay needed

    // fill in the password
    const passwordInput = await driver.findElement(By.id("password"));
    await passwordInput.sendKeys(process.env.PAYPAL_PASSWORD);
    await driver.sleep(500); // Delay needed
    // Click login button
    let btnLogin = await driver.findElement(By.id("btnLogin"));
    await btnLogin.click();

    //stop loading the page
    await driver.sleep(1000);
    await driver.executeScript("window.stop();");
    await driver.sleep(1000);
    await driver.executeScript("window.stop();");

    // find and click the latest payment in the list of payments
    let payment = await driver.findElement(
      By.className("counterparty_name css-1htline spf-1yo2lxy-text_body_strong")
    );

    await payment.click();

    await driver.sleep(4000); // Delay needed

    // decline cookies - this window was a bit annoying as usual
    let cookiesDeclineBtn = await driver.findElement(
      By.id("bannerDeclineButton")
    );
    await cookiesDeclineBtn.click();

    await driver.sleep(1500); // Delay needed

    // scroll until the customer transaction ID is visible
    await driver.executeScript(
      "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'start' });",
      await driver.wait(
        until.elementLocated(By.id("activity_paid_with_view")),
        20000
      )
    );

    // keep the value of the transaction id
    let transactionID = await driver
      .findElement(By.className("spf_text breakText"))
      .getText();

    await driver.sleep(1000);

    // visit the page in which you can submit a new dispute for this transaction
    await driver.get(
      `https://www.sandbox.paypal.com/resolutioncenter/filing/${transactionID}/create?type=PAYMENT`
    );

    // choose the type of your problem
    // const problemTypeBtn = await driver.findElement(
    //   By.css('button[data-testid="elg-item-1"]')
    // );
    let problemTypeBtn = await driver.wait(
      until.elementLocated(By.css('button[data-testid="elg-item-1"]')),
      25000
    );
    await driver.sleep(1000);
    await problemTypeBtn.click();

    await driver.sleep(1000); // Delay needed

    // scroll until all the inputs are visible
    await driver.executeScript(
      "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'start' });",
      await driver.findElement(By.className("step-title"))
    );

    await driver.sleep(1000); // Delay needed

    // find and click the button related to the type of the product
    const productTypeBtn = await driver.findElement(
      By.id("dropdownMenuButton_Τύποςπροϊόντος")
    );
    await productTypeBtn.click();

    await driver.sleep(1000); // Delay needed

    // find and click the desired option for product type
    const productTypeOption = await driver.findElement(
      By.id("smenu_item_PRODUCT")
    );
    await productTypeOption.click();

    await driver.sleep(1000); // Delay needed

    // find and click the button related to the category of the product
    const categoryBtn = await driver.findElement(
      By.id("dropdownMenuButton_Κατηγορία")
    );
    await categoryBtn.click();

    await driver.sleep(1000); // Delay needed

    // find and click the desired option for product's category
    const categoryOption = await driver.findElement(By.id("smenu_item_OTHER"));
    await categoryOption.click();

    await driver.sleep(1000); // Delay needed

    // click Next button
    const nextBtn = await driver.findElement(
      By.className("filing__step-continue-button")
    );
    await nextBtn.click();

    await driver.sleep(1000); // Delay needed

    // choose the option according to which the product was defective
    const defectiveProductOptionBtn = await driver.findElement(
      By.css('label[for="selection_items.0.subIssue_DEFECTIVE"]')
    );

    await defectiveProductOptionBtn.click();

    await driver.sleep(1000); // Delay needed

    // scroll until Next button is visible
    await driver.executeScript(
      "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'start' });",
      await driver.findElement(
        By.css('label[for="selection_items.0.subIssue_DEFECTIVE"]')
      )
    );

    await driver.sleep(1000); // Delay needed

    // click Next
    const NextBtn = await driver.findElement(
      By.className("filing__step-continue-button")
    );

    await NextBtn.click();

    await driver.sleep(1000); // Delay needed

    await driver.executeScript(
      "window.scrollTo({ top: 0, behavior: 'smooth' });"
    );

    await driver.sleep(1000); // Delay needed

    // Fill in with comments (>=120 characters)
    const commentsInput = await driver.findElement(
      By.id("text-input-items.0.notes")
    );
    await commentsInput.sendKeys(
      "commentscommentscommentscommentscommentscommentscommentscommentscommentscommentscommentscommentscommentscommentscomments"
    );

    await driver.sleep(1000); // Delay needed

    // scroll down
    await driver.executeScript(
      "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'start' });",
      await driver.findElement(By.className("additional-info__question"))
    );

    await driver.sleep(1000); // Delay needed

    // select the delivery date

    // Find the date picker input element
    const datePicker = await driver.findElement(
      By.id("text-input-dateSelector")
    );
    // Click on the date picker to open the calendar
    await datePicker.click();
    // Select a specific date
    const selectedDate = "07-08-2024";
    // Format the date for sending keys
    await datePicker.sendKeys(selectedDate, Key.ENTER);

    await driver.sleep(1000); // Delay needed

    // fill in the expected refund amount
    const refundAmountInput = await driver.findElement(
      By.id("text-input-items.0.expected_refund")
    );
    await refundAmountInput.sendKeys("80,00");

    await driver.sleep(500); // Delay needed

    // scroll down
    await driver.executeScript(
      "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'start' });",
      await driver.findElement(By.className("cw-footer"))
    );

    await driver.sleep(1000); // Delay needed

    // choose that you want to return the product back to the seller
    const returnOption = await driver.findElement(
      By.css(
        'label[for="selection_items.0.product_details.return_details.return_intent_RETURN"]'
      )
    );

    await returnOption.click();

    await driver.sleep(1000); // Delay needed

    // click Next button
    const NextButton = await driver.findElement(
      By.className("filing__step-continue-button")
    );

    await NextButton.click();

    await driver.sleep(1000); // Delay needed

    await driver.executeScript(
      "window.scrollTo({ top: 0, behavior: 'smooth' });"
    );

    await driver.sleep(1000); // Delay needed

    // choose that you have not yet contacted the merchant
    const noContactedOption = await driver.findElement(
      By.css('label[for="selection_merchant_contacted_NO"]')
    );

    await noContactedOption.click();

    await driver.sleep(1000); // Delay needed

    // click Next button
    const NextBttn = await driver.findElement(
      By.className("filing__step-continue-button")
    );

    await NextBttn.click();

    await driver.sleep(1000); // Delay needed

    // scroll down
    await driver.executeScript(
      "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'start' });",
      await driver.findElement(By.className("doc-upload__instruction-item"))
    );

    await driver.sleep(1000); // Delay needed

    // Add a file

    let fileInput = driver.findElement(By.css('input[type="file"]'));
    fileInput.sendKeys(path.resolve("./requests/selenium/images/image1.jpg"));

    await driver.sleep(3000); // Delay needed

    // add some extra info
    const extraInfoInput = await driver.findElement(By.id("text-input-notes"));
    await extraInfoInput.sendKeys("Some extra information");

    await driver.sleep(1000); // Delay needed

    // click Next button
    const SubmitBtn = await driver.findElement(
      By.className("filing__step-continue-button")
    );

    await SubmitBtn.click();

    await driver.sleep(4000); // Delay needed

    await driver.manage().setTimeouts({ implicit: 500 });
  } catch (e) {
    console.log(e);
  } finally {
    // close the browser
    await driver.quit();
  }
};

export const denyOffer = async (dispute_id) => {
  let driver;
  try {
    driver = await new Builder().forBrowser(Browser.CHROME).build();
    // Set the position and size of the browser window
    await driver
      .manage()
      .window()
      .setRect({ width: 1000, height: 950, x: 120, y: 50 });
    // visit approveLink URL
    await driver.get(
      `https://www.sandbox.paypal.com/resolutioncenter/view/${dispute_id}/inquiry`
    );

    // fill in the email
    let emailInput = await driver.findElement(By.id("email"));
    await emailInput.sendKeys(process.env.PAYPAL_EMAIL);
    await driver.sleep(500); // Delay needed
    // click Next button
    let nextButton = await driver.findElement(By.id("btnNext"));
    await nextButton.click();
    await driver.sleep(2500); // Delay needed

    // fill in the password
    const passwordInput = await driver.findElement(By.id("password"));
    await passwordInput.sendKeys(process.env.PAYPAL_PASSWORD);
    await driver.sleep(500); // Delay needed
    // Click login button
    let btnLogin = await driver.findElement(By.id("btnLogin"));
    await btnLogin.click();

    await driver.sleep(5000); // Delay needed

    // scroll down
    await driver.executeScript(
      "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'start' });",
      await driver.wait(
        until.elementLocated(By.className("chat-window__header-title ")),
        20000
      )
    );

    await driver.sleep(4000); // Delay needed

    // deny offer
    let denyOfferBtn = await driver.findElement(
      By.css('button[data-pa-click="Deny and send message"]')
    );
    await denyOfferBtn.click();

    await driver.sleep(1000); // Delay needed

    // fill in the reason why you deny the offer and submit
    let denyReasonInput = await driver.findElement(
      By.css('textarea[data-testid="note"]')
    );
    await denyReasonInput.clear();
    await denyReasonInput.sendKeys("refund offer is very low.");
    await driver.sleep(1000); // Delay needed
    let submitBtn = await driver.findElement(By.className("btn--block"));
    await submitBtn.click();

    await driver.sleep(3000); // Delay needed

    let finishBtn = await driver.findElement(
      By.className(" acknowledge__done")
    );
    await finishBtn.click();

    await driver.sleep(5000); // Delay needed

    await driver.manage().setTimeouts({ implicit: 500 });
  } catch (e) {
    console.log(e);
  } finally {
    // close the browser
    await driver.quit();
  }
};

// the buyer appeals the decision of the PayPal agent
export const buyerProvidesEvidence = async (dispute_id) => {
  let driver;
  try {
    driver = await new Builder().forBrowser(Browser.CHROME).build();
    // Set the position and size of the browser window
    await driver
      .manage()
      .window()
      .setRect({ width: 500, height: 1000, x: 120, y: 50 });
    // visit approveLink URL
    await driver.get(
      `https://www.sandbox.paypal.com/resolutioncenter/view/${dispute_id}/`
    );

    await driver.sleep(1000); // Delay needed

    // fill in the email
    let emailInput = await driver.findElement(By.id("email"));
    await emailInput.sendKeys(process.env.PAYPAL_EMAIL);
    await driver.sleep(500); // Delay needed
    // click Next button
    let nextButton = await driver.findElement(By.id("btnNext"));
    await nextButton.click();
    await driver.sleep(2500); // Delay needed

    // fill in the password
    const passwordInput = await driver.findElement(By.id("password"));
    await passwordInput.sendKeys(process.env.PAYPAL_PASSWORD);
    await driver.sleep(500); // Delay needed
    // Click login button
    let btnLogin = await driver.findElement(By.id("btnLogin"));
    await btnLogin.click();

    await driver.sleep(3000); // Delay needed

    // scroll down
    await driver.executeScript(
      "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'start' });",
      await driver.wait(
        until.elementLocated(By.className("list__wrapper")),
        25000
      )
    );

    await driver.sleep(1000); // Delay needed
    // Click login button
    let ReplyBtn = await driver.findElement(
      By.css('button[data-testid="respond"]')
    );
    await ReplyBtn.click();

    await driver.sleep(1000); // Delay needed

    // scroll down
    await driver.executeScript(
      "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'start' });",
      await driver.wait(
        until.elementLocated(By.className("additional-info__button")),
        25000
      )
    );

    await driver.sleep(1000); // Delay needed

    // upload file

    // Locate the file input element
    let fileInput = await driver.findElement(By.id("upload"));
    await fileInput.sendKeys(
      path.resolve("./requests/selenium/images/image1.jpg")
    );

    await driver.sleep(2000); // Delay needed

    // fill in your message
    let additionalInfoInput = await driver.findElement(
      By.css('textarea[data-testid="additional-info-note"]')
    );

    await additionalInfoInput.clear();
    await additionalInfoInput.sendKeys("You are wrong PayPal!");
    await driver.sleep(1000); // Delay needed

    // Click submit button
    let SubmitBtn = await driver.findElement(
      By.className("additional-info__button")
    );
    await SubmitBtn.click();
    await driver.sleep(3500); // Delay needed

    await driver.manage().setTimeouts({ implicit: 500 });
  } catch (e) {
    console.log(e);
  } finally {
    // close the browser
    // await driver.quit();
  }
};

// the buyer approves a subscription
export const approveSubscription = async (approveLink) => {
  let driver;
  try {
    driver = await new Builder().forBrowser(Browser.CHROME).build();
    // Set the position and size of the browser window
    await driver
      .manage()
      .window()
      .setRect({ width: 600, height: 900, x: 120, y: 50 });
    // visit approveLink URL
    await driver.get(approveLink);

    await driver.sleep(1000); // Delay needed

    // fill in the email
    let emailInput = await driver.findElement(By.id("email"));
    await emailInput.sendKeys(process.env.PAYPAL_EMAIL);
    await driver.sleep(500); // Delay needed
    // click Next button
    let nextButton = await driver.findElement(By.id("btnNext"));
    await nextButton.click();
    await driver.sleep(2500); // Delay needed

    // fill in the password
    const passwordInput = await driver.findElement(By.id("password"));
    await passwordInput.sendKeys(process.env.PAYPAL_PASSWORD);
    await driver.sleep(500); // Delay needed
    // Click login button
    let btnLogin = await driver.findElement(By.id("btnLogin"));
    await btnLogin.click();

    // Click accept button
    let submitBtn = await driver.wait(
      until.elementLocated(By.css('input[data-test-id="continueButton"]')),
      50000
    );
    await submitBtn.click();

    await driver.sleep(20000); // Delay needed

    await driver.manage().setTimeouts({ implicit: 500 });
  } catch (e) {
    console.log(e);
  } finally {
    // close the browser
    await driver.quit();
  }
};
