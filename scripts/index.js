import { useCase1cRequests } from "./requests/UseCase1cReqs.js";
import { useCase1Requests } from "./requests/UseCase1Reqs.js";

await useCase1Requests();
console.log("");
await useCase1cRequests();
