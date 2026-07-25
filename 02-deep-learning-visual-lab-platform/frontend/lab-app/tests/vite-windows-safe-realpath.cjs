/* eslint-disable @typescript-eslint/no-require-imports */
const childProcess = require("node:child_process");
const { EventEmitter } = require("node:events");
const { syncBuiltinESMExports } = require("node:module");

const originalExec = childProcess.exec;

childProcess.exec = function patchedExec(command, ...args) {
  if (command !== "net use") {
    return originalExec.call(this, command, ...args);
  }

  const callback = args.find((argument) => typeof argument === "function");
  const child = new EventEmitter();
  child.stdout = new EventEmitter();
  child.stderr = new EventEmitter();

  queueMicrotask(() => {
    if (callback) {
      callback(new Error("Network-drive discovery is unavailable."), "", "");
    }
    child.emit("close", 1);
  });
  return child;
};

syncBuiltinESMExports();
