
function _addBorderToTweets() {
  console.log("fired!!!!");

  $('div[lang="en"]').each(function() {
  // `this` is the div
  console.log(this.textContent);
  obj = this;

  $.ajax({
    type: "GET",
    url: "https://twitter-bert.ngrok.io/classify?tweet=" + this.textContent,
    async: false,
    dataType: "json",
    success: function (result, status, xhr) {
      console.log(result);
      if (result.scores.DISASTER >= 0.9) {
        console.log('RED')
        obj.style.border = "thick solid #ff0000";  // RED
      }
      else if (result.probability >= 0.5) {
        console.log('YELLOW')
        console.log(obj);
        obj.style.border = "thick solid #ffff00";  // YELLOW
      }
      else {
        console.log('GREEN')
        obj.style.border = "thick solid #00ff00";  // GREEN
      }

    },
    error: function (xhr, status, error) {
      console.log("Result: " + status + " " + error + " " + xhr.status + " " + xhr.statusText)
    }
  });

});
}

setInterval(_addBorderToTweets, 2000);  // run our ML code every 2 seconds
