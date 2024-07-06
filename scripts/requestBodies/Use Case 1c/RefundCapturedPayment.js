export const refundCapturedPaymentReqBody = {
  amount: {
    value: "80.00",
    currency_code: "USD",
  },
  invoice_id: `${Date.now()}`,
  note_to_payer: "Defective product",
};
