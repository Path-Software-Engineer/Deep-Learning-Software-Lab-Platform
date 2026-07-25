import path from "node:path";
import { fileURLToPath } from "node:url";
import ts from "typescript";
import { defineConfig } from "vitest/config";

const directory = path.dirname(fileURLToPath(import.meta.url));

const inProcessTypeScript = {
  name: "in-process-typescript",
  enforce: "pre",
  transform(source, id) {
    if (!/\.[cm]?tsx?$/.test(id) || id.includes("/node_modules/")) {
      return null;
    }
    const result = ts.transpileModule(source, {
      compilerOptions: {
        jsx: ts.JsxEmit.ReactJSX,
        module: ts.ModuleKind.ESNext,
        moduleResolution: ts.ModuleResolutionKind.Bundler,
        target: ts.ScriptTarget.ES2022,
        sourceMap: true
      },
      fileName: id
    });
    return {
      code: result.outputText,
      map: result.sourceMapText ?? null
    };
  }
};

export default defineConfig({
  esbuild: false,
  plugins: [inProcessTypeScript],
  resolve: {
    alias: {
      "@": directory
    }
  },
  test: {
    environment: "jsdom",
    setupFiles: ["./tests/setup.ts"],
    exclude: ["tests/e2e/**", "node_modules/**", ".next/**"],
    pool: "threads",
    fileParallelism: false,
    coverage: {
      reporter: ["text", "html"]
    }
  }
});
