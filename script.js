async function submitData() {
    const btn = document.querySelector('button');
    const resultDiv = document.getElementById('result');
    const statusText = document.getElementById('status-text');
    const feedbackText = document.getElementById('feedback-text');

    // 1. FIX: Safely capture and convert values
    // Using Number(...) || 0 ensures the JSON is never "empty"
    const payload = {
        student_id: Number(document.getElementById('student_id').value) || 0,
        topic: document.getElementById('topic').value || "General",
        question: document.getElementById('question').value || "No question provided",
        student_answer: document.getElementById('student_answer').value || "",
        correct_answer: document.getElementById('correct_answer').value || "",
        time_taken: Number(document.getElementById('time_taken').value) || 0
    };

    btn.disabled = true;
    btn.innerText = "Processing...";

    try {
        const response = await fetch('http://127.0.0.1:8000/submit-answer', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(payload) // This will now be valid JSON
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error("Server Error Details:", errorData);
            throw new Error(`Server responded with ${response.status}`);
        }

        const data = await response.json();

        resultDiv.style.display = 'block';
        if (data.correct) {
            resultDiv.className = 'correct';
            statusText.innerText = "✓ Correct!";
        } else {
            resultDiv.className = 'incorrect';
            statusText.innerText = "✕ Incorrect";
        }
        feedbackText.innerText = data.feedback;

    } catch (error) {
        console.error("Fetch Error:", error);
        alert("Submission failed. Check the browser console (F12) for details.");
    } finally {
        btn.disabled = false;
        btn.innerText = "Submit Answer";
    }
}