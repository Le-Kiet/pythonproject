var updateBtns = document.getElementsByClassName("update-cart");
var sortProducts = document.getElementsByClassName("update-cart");

for (i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    console.log(productId, "productId", action, "action");
    console.log("user:", user);
    if (user === "AnonymousUser") {
      console.log("user not logged in");
    } else {
      updateUserOrder(productId, action);
    }
  });
}

function updateUserOrder(productId, action) {
  console.log("user logged in, success added");
  var url = "/update_item/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      productId: productId,
      action: action,
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("data", data);
      location.reload();
    });
}
for (i = 0; i < sortProducts.length; i++) {
  sortProducts[i].addEventListener("click", function () {
    var sortValue = this.dataset.value;
    updateSortValue(sortValue);
  });
}

function updateSortValue(sortValue) {
  var url = new URL(window.location.href);
  url.searchParams.set("sort", sortValue);
  window.location.href = url.href;
}
