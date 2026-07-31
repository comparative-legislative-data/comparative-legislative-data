import { Matrix } from 'ml-matrix';
import LogisticRegression from 'ml-logistic-regression';

const logX = [
  [1, 0, 5],
  [1, 0, 5],
  [0, 1, 2],
  [0, 1, 2],
  [1, 0, 4],
  [0, 1, 1]
];

const logY = [
  [1], [1], [0], [0], [1], [0]
];

try {
  const xMatrix = new Matrix(logX);
  const yMatrix = new Matrix(logY);
  const logreg = new LogisticRegression({ numSteps: 100, learningRate: 5e-3 });
  logreg.train(xMatrix, yMatrix);
  console.log("Success", logreg.weights);
} catch(e) {
  console.log("Error!", e);
}
