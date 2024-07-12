const https = require('https');
const axios = require('axios');
const fs = require('fs');
const Request = require('../models/Requests');
const FormData = require('form-data');
const { inferType } = require("@jsonhero/json-infer-types");

const agent = new https.Agent({ rejectUnauthorized: false });

const formatDomain = (domain) => {
    if (!(domain.startsWith('http_') || domain.startsWith('https_'))) throw new Error('Invalid URL, should start with http_ or https_.');
    domain = domain.replace(/(http_)|(https_)/g, (match) => {
        if (match === "http_") return "http://";
        else if (match === "https_") return "https://";
    });
    return domain.replace(/_/g, '.');
};

const makeRequest = async (target, method, originalHeaders, body, files) => {
    let headers = {};
    for (let key of Object.keys(originalHeaders)) {
        if (!['host', 'content-length', 'transfer-encoding', 'connection'].includes(key.toLowerCase())) {
            headers[key] = originalHeaders[key];
        }
    }
    let options = { method, headers, httpsAgent: agent };
    
    if(files){
        const form = new FormData();
        // Add JSON fields to the form
        for (const key in body) {
            form.append(key, body[key],{
                contentType: "application/json",
            });
        }

        // Add the files to the form
        files.map((file) => (
            form.append(file.fieldname, fs.createReadStream(file.path), {
                filename: file.originalname,
            })
        ))
        
        options.data = form;
    }
    else{
        if (Object.keys(body).length !== 0) options.data = body;
    }

    return await axios(target, options);
};

function constructSchema(obj) {
    if (typeof obj !== 'object' || obj === null) {
        // Base case: if obj is not an object, return its inferred type
        return inferType(obj);
    }

    // If obj is an object, iterate over its properties
    const schema = {};
    for (const key in obj) {
        if (Object.prototype.hasOwnProperty.call(obj, key)) {
            // Recursively construct schema for nested properties
            schema[key] = constructSchema(obj[key]);
        }
    }
    return schema;
}

const saveRequest = async (ip, method, url, endpoint, headers, body, query, paramsArr, responseStatus, data) => {
    const requestSchema = constructSchema(data);
    const request = new Request({ ip, method, url, endpoint, headers, body, query,
        params: paramsArr,
        response: { responseStatus, requestSchema },
    });
    return await request.save();
};

exports.mim = async (req, res) => {
    const { ip, headers, method, query, files } = req;
    let body = req.body;
    const queryString = new URLSearchParams(query).toString();
    let params = req.params[0];
    let paramsArr = params.split('/');
    let domain = req.params.domain;

    try {
        domain = formatDomain(domain);
        const target = `${domain}/${params}${queryString ? `?${queryString}` : ''}`;
        const response = await makeRequest(target, method, headers, body, files);
        const { status: responseStatus, data } = response;
        if (files) files.map((file) => (body[file.fieldname] = file));
        const bodySchema = constructSchema(body);
        await saveRequest(ip, method, domain, params, headers, bodySchema, query, paramsArr, responseStatus, data);
        return res.status(responseStatus).json(data);
    } catch (e) {
        console.log(e.message);
        return res.status(500).json({ message: e.message || 'Internal server error.' });
    }
};