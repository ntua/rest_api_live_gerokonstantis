import { useCase1bRequests } from "./requests/UseCase1bReqs.js";
import { useCase1cRequests } from "./requests/UseCase1cReqs.js";
import { useCase1Requests } from "./requests/UseCase1Reqs.js";
import { useCase2bRequests } from "./requests/UseCase2bReqs.js";
import { useCase2Requests } from "./requests/UseCase2Reqs.js";
import { useCase3Requests } from "./requests/UseCase3Reqs.js";
import { useCase5Requests } from "./requests/UseCase5Reqs.js";
import { useCase6Requests } from "./requests/UseCase6Reqs.js";
import { useCase7Requests } from "./requests/UseCase7Reqs.js";
import { useCase8Requests } from "./requests/UseCase8Reqs.js";

await useCase1Requests();
console.log("");
await useCase1bRequests();
console.log("");
await useCase1cRequests();
console.log("");
await useCase2Requests();
console.log("");
await useCase2bRequests();
console.log("");
// await useCase3Requests();
// console.log("");
await useCase5Requests();
console.log("");
await useCase6Requests();
console.log("");
await useCase7Requests();
console.log("");
await useCase8Requests();
