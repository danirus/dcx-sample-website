function setLanguage(event) {
    event.preventDefault();
    const link = event.target;
    const form = document.getElementById("langform");
    let fields = {
        csrfmiddlewaretoken: form.elements['csrfmiddlewaretoken'].value,
        language: link.dataset.value,
        next: ""
    }
    let formBody = [];
    for (const field in fields) {
        let key = encodeURIComponent(field);
        let value = encodeURIComponent(fields[field]);
        formBody.push(`${key}=${value}`);
    }
    formBody = formBody.join("&");
    fetch('/i18n/setlang/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded;charset-UTF-8',
      },
      body: formBody
    }).then((d) => {
      console.log("Then...", d);
    });
}

initDropdown("language-dropdown", setLanguage);