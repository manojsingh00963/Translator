document.getElementById("translate-btn").addEventListener("click", async () => {
  const inputLanguage = document.getElementById("input-language").value;
  const outputLanguage = document.getElementById("output-language").value;
  const inputText = document.getElementById("input-text").value;

  console.log({ inputLanguage, outputLanguage, inputText }); // Debugging

  if (!inputText.trim()) {
    alert("Please enter some text to translate.");
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/translate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        inputLanguage,
        outputLanguage,
        text: inputText,
      }),
    });

    const data = await response.json();

    document.getElementById("output-text").innerText =
      data.translation || "Translation error.";
  } catch (error) {
    console.error("Error:", error);
    document.getElementById("output-text").innerText = "Translation error.";
  }
});
