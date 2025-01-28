document.addEventListener("DOMContentLoaded", () => {
  const commentForm = document.getElementById("commentForm");
  const reviewRes = document.getElementById("review-res");
  const reviewsContainer = document.querySelector(".comment-container"); // Cache this element
  const averageRating = document.querySelector(".d-flex > h6"); // Cache this element too

  commentForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(commentForm);

    try {
      const response = await fetch(commentForm.action, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        if (response.status === 400) {
          const data = await response.json();
          const errorMessages = Object.values(data.errors).flat().join("\n"); // Improved error message handling
          throw new Error(errorMessages);
        }
        throw new Error(
          `HTTP Error ${response.status}: ${response.statusText}`,
        ); // Include status text
      }

      const data = await response.json();

      if (data.bool) {
        reviewRes.textContent = "Review submitted successfully!";
        reviewRes.classList.add("text-success");
        reviewRes.classList.remove("text-danger"); // Remove any previous error class

        if (reviewsContainer) {
          // No need to check this inside the loop every time
          const newReview = document.createElement("div");
          const rating = data.context.rating;
          const starsHTML = generateStars(rating); // Use a helper function

          newReview.className =
            "single-comment justify-content-between d-flex mb-30";
          newReview.innerHTML = `
            <div class="user justify-content-between d-flex">
              <div class="thumb text-center">
                <img class="hover-img" src="${data.context.user_image}" alt="${data.context.user}'s profile picture" style="aspect-ratio: 1/1; object-fit: cover;">  </img>
                <br>
                <a href="#" class="font-heading text-brand">${data.context.user}</a>
              </div>
              <div class="desc">
                <div class="d-flex justify-content-between mb-10">
                  <div class="d-flex align-items-center">
                    <span class="font-xs text-muted">${data.context.data}</span>
                  </div>
                  ${starsHTML}
                </div>
                <p class="mb-10">${data.context.review}</p>
              </div>
            </div>
          `;
          reviewsContainer.prepend(newReview);

          if (averageRating) {
            // No need to check this inside the loop every time
            averageRating.textContent = `${Number.parseFloat(data.context.average_rating).toFixed(1)} out of 5.0`;
          }
        }

        commentForm.reset();
      } else {
        reviewRes.textContent = "Error submitting review. Please try again.";
        reviewRes.classList.add("text-danger");
        reviewRes.classList.remove("text-success"); // Remove any previous success class
        console.error("Error:", data.errors);
      }
    } catch (error) {
      reviewRes.textContent = `Error: ${error.message}`;
      reviewRes.classList.add("text-danger");
      reviewRes.classList.remove("text-success"); // Remove any previous success class
      console.error("Error:", error);
    }
  });

  // Helper function to generate star HTML
  function generateStars(rating) {
    let starsHTML = "";
    for (let i = 1; i <= 5; i++) {
      starsHTML += `<i class="fas fa-star ${i <= rating ? "text-warning" : "text-secondary"}"></i>`;
    }
    return starsHTML;
  }
});

$(document).ready(function () {
  $(".filter-checkbox, #price-filter-btn").on("click", function () {
    console.log("Um checkbox foi selecionado");

    let filter_object = {};

    let min_price = $("#max_price").attr("min");
    let max_price = $("#max_price").val();

    filter_object.min_price = min_price;
    filter_object.max_price = max_price;

    $(".filter-checkbox").each(function () {
      let filter_value = $(this).val();
      let filter_key = $(this).data("filter");

      console.log("Filter value is:", filter_value);
      console.log("Filter key is:", filter_key);

      filter_object[filter_key] = Array.from(
        document.querySelectorAll(
          "input[data-filter=" + filter_key + "]:checked",
        ),
      ).map(function (element) {
        return element.value;
      });
    });
    console.log("Filter Object is: ", filter_object);
    $.ajax({
      url: "/filter-products",
      data: filter_object,
      dataType: "json",
      beforeSend: function () {
        console.log("Tentando filtrar produtos...");
      },
      success: function (response) {
        console.log(response);
        console.log("Filtragem de dados realizada com sucesso.");
        $("#filtered-product").html(response.data);
      },
    });
  });

  $("#max_price").on("blur", function () {
    let min_price = $(this).attr("min");
    let max_price = $(this).attr("max");
    let current_price = $(this).val();

    //console.log("O valor atual é de:", current_price);
    //console.log("O valor máximo é de:", max_price);
    //console.log("O valor mínimo é de:", min_price);

    if (
      current_price < parseInt(min_price) ||
      current_price > parseInt(max_price)
    ) {
      //console.log("Deu erro de preço, amigo! Arruma isso aí.");

      min_price = Math.round(min_price * 100) / 100;
      max_price = Math.round(max_price * 100) / 100;

      //console.log("O valor máximo é de:", max_Price);
      //console.log("O valor mínimo é de:", min_Price);

      alert("O preço deve estar entre R$" + min_price + " e R$" + max_price);
      $(this).val(min_price);

      $("#range").val(min_price);

      $(this).focus();

      return false;
    }
  });
});

$(".add-to-cart-btn").on("click", function () {
  let this_val = $(this);
  let index = this_val.attr("data-index");
  let quantity = $(".product-quantity-" + index).val();
  let product_title = $(".product-title-" + index).val();
  let product_image = $(".product-image-" + index).val();
  let product_pid = $(".product-pid-" + index).val();
  let product_id = $(".product-id-" + index).val();
  let product_price = $(".current-product-price-" + index).text();

  console.log("Quantidade:", quantity);
  console.log("Id:", product_id);
  console.log("PID:", product_pid);
  console.log("Titulo:", product_title);
  console.log("Imagem:", product_image);
  console.log("Index:", index);
  console.log("Preço:", product_price);
  console.log("Esse é:", this_val);

  $.ajax({
    url: "/add-to-cart",
    data: {
      id: product_id,
      pid: product_pid,
      image: product_image,
      qty: quantity,
      title: product_title,
      price: product_price,
    },
    dataType: "json",
    beforeSend: () => {
      console.log("Adicionando produtos ao Carrinho...");
    },
    success: (res) => {
      this_val.html("✔");
      console.log("Produtos adicionados ao Carrinho.");
      $(".cart-items-count").text(res.totalcartitems);
      this_val.attr("disabled", false);
    },
  });
});

$(document).ready(function () {
  $("#cart-list").on("click", ".delete-product", function (event) {
    event.preventDefault();
    const product_id = $(this).data("product");
    const $thisRow = $(this).closest("tr");

    $.ajax({
      url: "/delete-item-from-cart",
      method: "GET",
      data: { id: product_id },
      dataType: "json",
      beforeSend: () => {
        $thisRow.fadeOut();
      },
      success: (response) => {
        $("#cart-list").html(response.data);
        $(".cart-items-count").text(response.totalcartitems);
      },
      error: (error) => {
        console.error("Error deleting item:", error);
        alert(
          "Erro ao deletar item. Tente novamente. Detalhes do erro no console.",
        );
        $thisRow.fadeIn();
      },
    });
  });
});

$(document).ready(function () {
  $("#cart-list").on("click", ".qty-up, .qty-down", function (event) {
    event.preventDefault();
    const $button = $(this);
    const $row = $button.closest("tr");
    const $qtyInput = $row.find(".qty-val");
    const productId = $qtyInput.data("product-id");
    let quantity = parseInt($qtyInput.val(), 10);

    if ($button.hasClass("qty-up")) {
      quantity++;
    } else {
      quantity = Math.max(1, quantity - 1);
    }

    $qtyInput.val(quantity);

    $.ajax({
      url: "/update-cart/",
      method: "POST",
      data: { id: productId, quantity: quantity },
      dataType: "json",
      beforeSend: function (xhr) {
        const csrftoken = getCookie("csrftoken");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      },
      success: function (response) {
        const subtotalElement = $(`#subtotal-${response.product_id}`);
        const cartTotalElement = $(".cart_total_amount h4");
        const cartItemCountElement = $(".cart-items-count");

        if (
          subtotalElement.length &&
          cartTotalElement.length &&
          cartItemCountElement.length
        ) {
          subtotalElement.text(`R$ ${response.subtotal.toFixed(2)}`);
          cartTotalElement.text(`R$ ${response.cart_total_amount.toFixed(2)}`);
          cartItemCountElement.text(response.totalcartitems);
        } else {
          console.error("Error: Could not find elements to update.");
          alert("An unexpected error occurred. Please try again.");
        }
      },
      error: function (error) {
        console.error("Error updating cart:", error);
        alert("Error updating cart item.");
      },
    });
  });

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});

$(document).on("click", ".make-default-address", function () {
  const id = $(this).data("address-id");
  if (id) {
    console.log("The ID is:", id);
    console.log("The element is:", this);

    // Update visual selection *before* AJAX request
    $(".address-item").removeClass("default-address");
    $(`.address-item[data-address-id="${id}"]`).addClass("default-address");
    $(".current-default").text("");
    $(`.address-item[data-address-id="${id}"i] .current-default`).text(
      "Default Address",
    );
    $(`.check${id}`).show();
    $(`.button${id}`).hide();

    $.ajax({
      url: "/make-address-default/",
      type: "POST",
      data: { id: id },
      dataType: "json",
      beforeSend: (xhr) => {
        const csrftoken = getCookie("csrftoken");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      },
      success: (response) => {
        console.log("Address set as default:", response);
        if (!response.success) {
          // Handle unsuccessful response: Show an error message.
          alert(
            response.error ||
              "Failed to set address as default. Please try again.",
          );
        }
      },
      error: (error) => {
        let errorMessage =
          "Failed to set address as default. Please try again.";
        if (error.responseJSON?.error) {
          errorMessage = error.responseJSON.error;
        } else if (error.status === 404) {
          errorMessage = "Address not found";
        } else if (error.status === 400) {
          errorMessage = "Invalid 'id' parameter or missing 'id' parameter";
        } else if (error.status === 405) {
          errorMessage = "Invalid request method";
        }
        console.error("Error setting default address:", error);
        // Handle AJAX errors: Show an error message.
        alert(errorMessage);
      },
    });
  } else {
    console.error("Data attribute 'data-address-id' is missing!");
  }
});

$(document).on("click", ".delete-address", function () {
  const id = $(this).data("address-id");
  if (id) {
    if (confirm("Tem certeza que deseja deletar este endereço?")) {
      $.ajax({
        url: "/delete-address/",
        type: "POST",
        data: { id: id },
        dataType: "json",
        beforeSend: (xhr) => {
          const csrftoken = getCookie("csrftoken");
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: (response) => {
          if (response.success) {
            $(`.address-item[data-address-id="${id}"]`).fadeOut(
              300,
              function () {
                $(this).remove();
              },
            );
            alert("Endereço deletado com sucesso!");
          } else {
            alert(
              response.error || "Erro ao deletar endereço. Tente novamente.",
            );
          }
        },
        error: (error) => {
          console.error("Error deleting address:", error);
          alert(
            "Erro ao deletar endereço. Verifique sua conexão com a internet.",
          );
        },
      });
    }
  } else {
    console.error("Data attribute 'data-address-id' is missing!");
  }
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === `${name}=`) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}



document.addEventListener("DOMContentLoaded", () => {
  const quickviewButtons = document.querySelectorAll(".quickview-button");

  quickviewButtons.forEach((button) => {
    button.addEventListener("click", (e) => {
      e.preventDefault();
      const pid = button.dataset.pid;

      fetch(`/quickview/${pid}/`)
        .then((response) => {
          if (!response.ok) {
            throw new Error(
              `HTTP error! status: ${response.status} - ${response.statusText}`,
            );
          }
          return response.json();
        })
        .then((data) => {
          // Construindo o HTML dinamicamente - adaptado para o seu layout
          const productHTML = `
                        <div class="row">
                            <div class="col-md-6">
                                <img src="${data.imagem}" alt="${data.titulo}" style="max-width:100%;">
                            </div>
                            <div class="col-md-6">
                                <h3>${data.titulo}</h3>
                                <p>Preço: R$ ${data.preco}</p>
                                <p>Preço Antigo: R$ ${data.preco_antigo}</p>
                                <p>Vendedor: ${data.vendedor}</p>
                                <p>Categoria: ${data.categoria}</p>
                                <p>${data.descricao}</p>
                                <button type="button" class="btn btn-primary">Adicionar ao Carrinho</button>
                            </div>
                        </div>
                    `;
          const modalBody = $("#quickViewModal .modal-body");
          modalBody.html(productHTML);
          $("#quickViewModal").modal("show");
        })
        .catch((error) => {
          console.error("Error fetching product details:", error);
          const modalBody = $("#quickViewModal .modal-body");
          modalBody.html(
            `<p class="text-danger">Erro ao carregar a visualização rápida: ${error.message}</p>`,
          );
          $("#quickViewModal").modal("show");
        });
    });
  });
});

$(document).on("click", ".add-to-wishlist", function () {
  let product_id = $(this).attr("data-product-item");
  let this_val = $(this);

  console.log("O ID é:", product_id);
  console.log("O Elemento é:", this_val);

  // Input validation: Check if product_id is a valid number
  if (!/^\d+$/.test(product_id)) {
    console.error("Invalid product ID:", product_id);
    alert("Invalid product ID. Please try again.");
    return; // Stop further execution
  }

  $.ajax({
    url: "add-to-wishlist/",
    data: { id: parseInt(product_id, 10) }, // Parse product_id as integer
    method: "GET",
    success: function (response) {
      if (response.bool) {
        console.log("Produto adicionado à lista de desejos:", response.message);
        this_val.html("✔");
      } else {
        console.error(
          "Erro ao adicionar produto à lista de desejos:",
          response.message,
        );
        alert(response.message);
      }
    },
    error: function (error) {
      console.error("Erro ao adicionar produto à lista de desejos:", error);
      // Provide a more user-friendly error message
      alert(
        "Erro ao adicionar produto à lista de desejos. Tente novamente mais tarde.",
      );
    },
  });
});

$(document).on("click", ".delete-wishlist-product", function (event) {
  event.preventDefault(); // Prevent default form submission behavior
  const id = $(this).data("wishlist-product");
  const $thisRow = $(this).closest(".wishlist-item"); // Select the closest wishlist item

  if (id) {
    if (
      confirm("Tem certeza que deseja deletar este item da lista de desejos?")
    ) {
      $.ajax({
        url: "/delete-wishlist-item/",
        type: "POST",
        data: { id: id },
        dataType: "json",
        beforeSend: (xhr) => {
          const csrftoken = getCookie("csrftoken");
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: (response) => {
          if (response.success) {
            $thisRow.fadeOut(300, function () {
              $(this).remove(); // Remove the row after fade out completes
            });
            //alert("Item deletado da lista de desejos com sucesso!"); // Removed alert for real-time effect
          } else {
            alert(
              response.message ||
                "Erro ao deletar item da lista de desejos. Tente novamente.",
            );
          }
        },
        error: (error) => {
          console.error("Error deleting wishlist item:", error);
          alert(
            "Erro ao deletar item da lista de desejos. Verifique sua conexão com a internet.",
          );
        },
      });
    }
  } else {
    console.error("Data attribute 'data-wishlist-product' is missing!");
  }
});

$(document).on("submit", "#contact-form-ajax", (e) => {
  e.preventDefault();
  console.log("Enviado...");

  const nome = $("#nome").val();
  const email = $("#email").val();
  const telefone = $("#telefone").val();
  const assunto = $("#assunto").val();
  const mensagem = $("#mensagem").val();

  console.log("Nome:", nome);
  console.log("Email:", email);
  console.log("Telefone:", telefone);
  console.log("Assunto:", assunto);
  console.log("Mensagem:", mensagem);

  $.ajax({
    url: "/ajax-contato",
    method: "POST",
    data: {
      nome: nome,
      email: email,
      telefone: telefone,
      assunto: assunto,
      mensagem: mensagem,
    },
    dataType: "json",
    beforeSend: (xhr) => {
      const csrftoken = getCookie("csrftoken");
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    success: (response) => {
      if (response.success) {
        alert("Mensagem enviada com sucesso!");
        $("#contact-form-ajax")[0].reset(); // Reset the form
        $("#contact-form-ajax").hide(); // Hide the form
      } else {
        alert(response.message || "Erro ao enviar mensagem. Tente novamente.");
      }
    },
    error: (error) => {
      console.error("Error sending contact form:", error);
      alert("Erro ao enviar mensagem. Verifique sua conexão com a internet.");
    },
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const quickviewButtons = document.querySelectorAll(".quickview-button");

  quickviewButtons.forEach((button) => {
    button.addEventListener("click", (e) => {
      e.preventDefault();
      const pid = button.dataset.pid;

      fetch(`/quickview/${pid}/`)
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          // Construa o HTML do modal com os dados do produto
          const productHTML = `
                        <div class="row">
                            <div class="col-md-6">
                                <div class="product-image">
                                    <img src="${data.imagem}" alt="${data.titulo}" class="img-fluid">
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="product-info">
                                    <h2 class="product-title">${data.titulo}</h2>
                                    <div class="product-price">
                                        ${data.preco_antigo ? `<del>R$ ${data.preco_antigo}</del>` : ""}
                                        <span class="current-price">R$ ${data.preco}</span>
                                        ${
                                          data.porcentagem_desconto !== "0%"
                                            ? `<span class="discount-badge">${data.porcentagem_desconto}</span>`
                                            : ""
                                        }
                                    </div>
                                    <div class="product-meta">
                                        <span class="category">Categoria: ${data.categoria}</span>
                                        <span class="vendor">Vendedor: ${data.vendedor}</span>
                                    </div>
                                    <div class="product-description">
                                        ${data.descricao}
                                    </div>
                                    <div class="stock-status">
                                        ${
                                          data.em_estoque
                                            ? `<span class="in-stock">Em estoque (${data.qtd_estoque})</span>`
                                            : '<span class="out-of-stock">Fora de estoque</span>'
                                        }
                                    </div>
                                    <div class="product-actions">
                                        <button class="add-to-cart-btn btn btn-primary">
                                            Adicionar ao Carrinho
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;

          // Insira o HTML no modal e mostre-o
          const modalBody = document.querySelector(
            "#quickViewModal .modal-body",
          );
          modalBody.innerHTML = productHTML;

          // Inicialize o modal (assumindo que você está usando Bootstrap)
          const modal = new bootstrap.Modal(
            document.getElementById("quickViewModal"),
          );
          modal.show();
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("Erro ao carregar dados do produto");
        });
    });
  });
});
