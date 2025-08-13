document.addEventListener('DOMContentLoaded', function() {
    // --- Answer Modal Logic ---
    const answerModal = document.getElementById('answer-modal');
    const closeModal = document.querySelector('.close-button');
    const answerForm = document.getElementById('answer-form');
    const answerTextarea = document.getElementById('answer-textarea');
    const questionIdField = document.getElementById('question-id-field');

    // Function to open the modal
    window.openAnswerModal = function(questionId, questionText) {
        questionIdField.value = questionId;
        document.getElementById('modal-question-text').innerText = questionText;
        answerTextarea.value = ''; // Clear previous answer
        answerModal.style.display = 'block';
    }

    // Function to close the modal
    if(closeModal) {
        closeModal.onclick = function() {
            answerModal.style.display = 'none';
        }
    }

    // Close modal if user clicks outside of it
    window.onclick = function(event) {
        if (event.target == answerModal) {
            answerModal.style.display = 'none';
        }
    }

    // Handle form submission
    if(answerForm) {
        answerForm.onsubmit = async function(event) {
            event.preventDefault();
            const questionId = questionIdField.value;
            const answerText = answerTextarea.value;

            if (!answerText.trim()) {
                alert('Answer cannot be empty.');
                return;
            }

            try {
                const response = await fetch(`/admin/questions/${questionId}/answer`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ answer_text: answerText }),
                });

                if (response.ok) {
                    alert('Answer submitted successfully!');
                    // Reload the page to see the updated list
                    window.location.reload();
                } else {
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail || 'Failed to submit answer.'}`);
                }
            } catch (error) {
                console.error('Error submitting answer:', error);
                alert('An unexpected error occurred.');
            }
        }
    }

    // --- Delete Logic ---
    window.deleteQuestion = async function(questionId) {
        if (!confirm(`Are you sure you want to delete question ${questionId}? This cannot be undone.`)) {
            return;
        }

        // The delete functionality is a placeholder on the backend,
        // so this will currently just show the WIP message.
        try {
            const response = await fetch(`/admin/questions/${questionId}`, {
                method: 'DELETE',
            });
            const result = await response.json();
            alert(result.message);
            if(response.ok) {
                window.location.reload();
            }
        } catch (error) {
            console.error('Error deleting question:', error);
            alert('An unexpected error occurred.');
        }
    }

    // --- Success Story Logic ---
    window.approveStory = async function(storyId) {
        if (!confirm(`Are you sure you want to approve story ${storyId}?`)) {
            return;
        }
        try {
            const response = await fetch(`/admin/stories/${storyId}/approve`, {
                method: 'POST',
            });
            if(response.ok) {
                alert('Story approved successfully!');
                window.location.reload();
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.detail || 'Failed to approve story.'}`);
            }
        } catch (error) {
            console.error('Error approving story:', error);
            alert('An unexpected error occurred.');
        }
    }

    window.deleteStory = async function(storyId) {
        if (!confirm(`Are you sure you want to delete story ${storyId}?`)) {
            return;
        }
        try {
            const response = await fetch(`/admin/stories/${storyId}`, {
                method: 'DELETE',
            });
            const result = await response.json();
            alert(result.message);
             if(response.ok) {
                window.location.reload();
            }
        } catch (error) {
            console.error('Error deleting story:', error);
            alert('An unexpected error occurred.');
        }
    }

    // --- Table Filter Logic ---
    window.filterTable = function(inputId, tableId) {
        const input = document.getElementById(inputId);
        const filter = input.value.toUpperCase();
        const table = document.getElementById(tableId);
        const tr = table.getElementsByTagName("tr");

        for (let i = 1; i < tr.length; i++) { // Start from 1 to skip header row
            let td, i, txtValue;
            let display = "none";
            let tds = tr[i].getElementsByTagName("td");
            for (let j = 0; j < tds.length; j++) {
                td = tds[j];
                if (td) {
                    txtValue = td.textContent || td.innerText;
                    if (txtValue.toUpperCase().indexOf(filter) > -1) {
                        display = "";
                        break; // Show row if any cell matches
                    }
                }
            }
            tr[i].style.display = display;
        }
    }
});
