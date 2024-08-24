# Dynamic API analysis : Man In the Middle (MIM)
This repo contains the source code for the **_Man in the Middle_** (MIM) software that was developed as a part of a tool for dynamic API dependency analysis. 

## Description
MIM is designed to capture and store requests made to an API while undertaking itself to forward them to the API and receive the response. In this way, MIM operates as a mediator between the client and the API. 
The client sends API requests to MIM, MIM forwards them to the API and receives the response, stores information about the API call and returns the response to the client. This process is illustrated in the sequence diagram shown below.

<p align="center"><img src="https://github.com/user-attachments/assets/9c786206-ad8d-4154-8361-6ed280994382" width="600" height="280" /></p>

The information stored by MIM is in the form shown below :
- **ip** : the client's ip
- **method** : the HTTP method of the request
- **url** : the API's url
- **endpoint** : the API endpoint that accepts the request
- **headers** : the list of request's headers and their values
- **body** : the request body
- **query** : the query params (if available)
- **params** : the path's segments (including the path parameters)
- **response** : the response body
- **tag** : a label associated with the call (for example, the use case number to which this call belongs)
  

<p align="center"><img src="https://github.com/user-attachments/assets/be0ee5ed-e2fd-4776-b18a-cc927242a227" width="400" height="230" /></p>

## When and How to use MIM
It is important to note that MIM has to be placed between an API client and an API server accessible to the client. If the API is protected by a firewall and the client is not allowed to use it, MIM will not be able to forward and capture the network traffic. If the purpose is to work with a public and accessible API, the MIM can be set up locally. If the API of interest is a private enterprise API, MIM has to be set up in the appropriate private network.

## Set up (locally) and use MIM
The prerequisite for running MIM is that you already have the [Docker environment](https://docs.docker.com/engine/install/) installed. If so, it is only necessary to move to the **mim** directory and run
`(sudo) docker-compose up`
After that, MIM will be running locally on port 3003.

### Make an API call using MIM
Assume we want to make a call to the PayPal sandbox API. Specifically, it is required to make the call :
```
PUT https://api-m.sandbox.paypal.com/v2/invoicing/invoices/INV2-J43G-QASS-VQZX-HRL2?send_to_recipient=true&send_to_invoicer=true
```

in order to update an invoice. The MIM endpoint used to forward and store the network traffic is the
`/proxy/:domain/:tag/*` where **_domain_** specifies the url of the API and **_tag_** specifies a (user defined) label associated with the call. 

If the desired tag is "usecase42", it is only needed to configure a call with the appropriate request body, headers, authorization tokens etc (either by using a tool like Postman or by writing a script in a programming language like js or python) and replace the previous URL with the one shown below : 
```
PUT http://localhost:3003/proxy/https_api-m_sandbox_paypal_com/usecase42/v2/invoicing/invoices/INV2-J43G-QASS-VQZX-HRL2?send_to_recipient=true&send_to_invoicer=true
```
Notice how the domain is passed into the URL. The symbols `://` have to be replaced with underscore and any following dot is also replaced with underscore.
### Export API calls
MIM provides one more useful endpoint for exporting the records associated with a specific API : `proxy_utils/export/:domain`. If there is a need to export all the records associated with the PayPal API (url : `https://api-m.sandbox.paypal.com`), you can just make a GET request as shown below (you can only use a browser to make this GET request):
```
GET http://localhost:3003/proxy_utils/export/https_api-m_sandbox_paypal_com
```
After that, the created .json file will be saved in the directory `/mim/downloads`. 

## Paypal Scripts
For testing purposes, in the `/paypal scripts` directory, a set of scripts that execute some possible PayPal API use cases is also available. Once MIM is set up and running (locally on port 3003), move to the `/paypal scripts` directory and run `npm install` so as to install the necessary packages. In order to run the scripts, use the command :
```
node index.js [arguments]
```
**_arguments_** is a list of space separated use case identifiers. With `node index.js all`, all the available use cases will be executed. With `node index.js 3 4`, use cases 3 and 4 will be executed. The available use cases along with their identifiers are shown below:
- **1** : The seller can create a new product and a new order for that product. The buyer pays for this order and the seller adds tracking information related to this order.
- **1b** : An order is created. The payment is authorized and then canceled.
- **1c** : The seller creates a new product and a new order for that product. The payment is captured and a refund is made.
- **2** : The seller creates two products and an invoice containing these two items. The buyer pays and then the invoice is canceled and deleted by the seller.
- **2b** : An invoice is created and sent to the buyer. The buyer pays, but the payment is deleted. The client tries to pay again and then the seller refunds the payment.
- **3** : The seller creates a new order, the buyer pays for it and tracking information is added. The buyer makes a dispute and the seller makes an offer to resolve the dispute. The buyer denies the offer and the seller sends a message to the buyer to discuss about the issue. The discussion was unsuccessful and the seller escalates the dispute to claim (i.e. a PayPal agent will handle the dispute's resolution). The seller and the buyer provide evidence and extra information to defend themselves and the PayPal agent makes a decision in favor of the buyer (i.e. full refund). The seller appeals the decision and the agent updates the decision in favor of the seller.
- **3b** : The seller creates a new order and the buyer pays for it. The buyer makes a dispute and the seller makes an offer to resolve the dispute. The buyer accepts the offer and returns the item back. The seller confirms that the product was returned back.
- **4** : The seller can create an order for a product, authorize and capture the payment for this order. The buyer submits a dispute and the seller accepts it. The item is returned back to the seller.
- **5** : The seller creates a monthly billing plan and a subscription for a newly created product.
- **6** : A user makes payments to multiple PayPal recipients at once. After getting details about these payments, the user cancels unclaimed payout items.
- **7** : A webhook is configured so as to subscribe webhook listeners to events. Αn order is then created and a payment is captured. This event is captured by the webhook and a notification to the webhook listener app is generated.
After that, we test the webhook by triggering a sample event and simulating the webhook with a "CUSTOMER.DISPUTE.CREATED" event.
The Webhook is updated so as not to capture all possible events and finally the webhook is deleted.
- **8** : An invoice template is created and after retrieving details, it is updated and then deleted.

