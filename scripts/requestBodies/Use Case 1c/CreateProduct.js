export const CreateProductReqBody = {
  name: "My Product 1",
  type: "PHYSICAL",
  id: `${Date.now()}`,
  description: "Product's description 1",
  category: "CLOTHING",
  image_url: `https://example.com/gallary/images/${Date.now()}.jpg`,
  home_url: `https://example.com/catalog/${Date.now()}.jpg`,
};
