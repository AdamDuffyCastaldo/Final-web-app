function deleteNote(noteId) {
    fetch("/deletenote", {
        method: "POST",
        body: JSON.stringify({noteId: noteId}),
    }).then((_res) => {
        window.location.href = "/";
    });
}