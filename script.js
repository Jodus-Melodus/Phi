// Your Markdown content
const markdownText = `# Hello, Markdown!
This is a **markdown** file.`;

// Create a new Showdown converter
const converter = new showdown.Converter();

// Convert Markdown to HTML
const htmlContent = converter.makeHtml(markdownText);

// Insert the HTML content into the specified div
document.getElementById('syntax').innerHTML = htmlContent;