// fix-symbols-with-openai.js
const fs = require("fs");
const { Configuration, OpenAIApi } = require("openai");

const config = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
});

const openai = new OpenAIApi(config);

// Load file with symbol errors
const code = fs.readFileSync("path/to/code-with-errors.js", "utf-8");
const errorLog = fs.readFileSync("symbol-errors.txt", "utf-8");

async function fixCode() {
  const prompt = `
You are a helpful coding assistant. Here's a JavaScript file and its symbol errors.
Fix only symbol-related issues without changing logic.

Code:
${code}

Errors:
${errorLog}

Correct the code:
`;

  const res = await openai.createChatCompletion({
    model: "gpt-4",
    messages: [{ role: "user", content: prompt }],
    temperature: 0.2,
  });

  const fixedCode = res.data.choices[0].message.content;
  fs.writeFileSync("path/to/code-with-errors.js", fixedCode);
  console.log("Code fixed by OpenAI!");
}

fixCode();
