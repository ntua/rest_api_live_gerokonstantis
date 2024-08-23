# Dynamic API analysis : Man In the Middle (MIM)
This repo contains the source code for the **_Man in the Middle_** (MIM) software that was developed as a part of a tool for dynamic API dependency analysis. 

## Description
MIM is designed to capture and store requests made to an API before undertaking itself to forward them to the API. In this way, MIM operates as a mediator between the client and the API. 
The client sends API requests to MIM, MIM forwards them to the API and receives the response, stores information about the API call and returns the response to the client. This process is illustrated in the sequence diagram below.

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
The prerequisite for running MIM is that you already have the Docker environment installed. If so, it is only necessary to move to the **mim** directory and run
`(sudo) docker-compose up`
After that, MIM will be running locally on port 3003.

### Make an API call using MIM
Assume we want to make a call to the PayPal sandbox API. Specifically, it is required to make the call :
```
PUT https://api-m.sandbox.paypal.com/v2/invoicing/invoices/INV2-J43G-QASS-VQZX-HRL2?send_to_recipient=true&send_to_invoicer=true
```

in order to update an invoice. The MIM endpoint used to forward and store the network traffic is the
`/proxy/:domain/:tag/*` where **_domain_** specifies the url of the API and **_tag_** specifies a label associated with the call. 

If the desired tag is "jimmy", it is only needed to configure a call with the appropriate request body, headers, authorization tokens etc (either by using a tool like Postman or by writing a script in a programming language like js or python) and replace the previous URL with the one below : 
```
PUT http://localhost:3003/proxy/https_api-m_sandbox_paypal_com/jimmy/v2/invoicing/invoices/INV2-J43G-QASS-VQZX-HRL2?send_to_recipient=true&send_to_invoicer=true
```
Pay attention to the way in which the domain is passed into the URL. The symbols `://` have to be replaced with underscore and any following dot is also replaced with underscore.
### Export API calls
MIM provides one more usefull endpoint for exporting the records associated with a specific API : `proxy_utils/export/:domain`. If there is a need to export all the records associated with the PayPal API (url : `https://api-m.sandbox.paypal.com`), you can just make a GET request as below (you can only use a browser to make this GET request):
```
GET http://localhost:3003/proxy_utils/export/https_api-m_sandbox_paypal_com
```
After that, the created .json file will be saved in the directory `/mim/downloads`. 


