({
    "name": "John",
    "uppercase": function(text) {
      return function (text, render) {
        return render(text.toUpperCase());
      }
    }
})