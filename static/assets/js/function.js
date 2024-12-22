document.addEventListener("DOMContentLoaded", () => {
  // Seleciona o formulário de comentários e o elemento para exibir mensagens de resposta.
  const commentForm = document.getElementById("commentForm");
  const reviewRes = document.getElementById("review-res");

  // Adiciona um event listener ao formulário de comentários para o evento 'submit'.
  commentForm.addEventListener("submit", async (event) => {
    // Impede o comportamento padrão do formulário (recarregamento da página).
    event.preventDefault();

    // Cria um FormData a partir dos dados do formulário.
    const formData = new FormData(commentForm);
    // Bloco try...catch para lidar com possíveis erros durante a requisição.
    try {
      // Faz uma requisição POST para o endpoint especificado no atributo 'action' do formulário.
      const response = await fetch(commentForm.action, {
        method: "POST",
        body: formData,
      });

      // Verifica se a resposta HTTP indica sucesso (status code 200-299).
      if (!response.ok) {
        // Se a resposta não for OK, verifica o código de status.
        if (response.status === 400) {
          // Se o código de status for 400 (Bad Request), analisa a resposta JSON para obter mensagens de erro.
          const data = await response.json();
          let errorMessages = "";
          for (const field in data.errors) {
            errorMessages += `${field}: ${data.errors[field][0]}\n`;
          }
          // Lança um novo erro com as mensagens de erro concatenadas.
          throw new Error(errorMessages);
        }
        // Para outros códigos de status de erro, lança um erro com a mensagem de erro HTTP.
        throw new Error(`Erro HTTP ${response.status}`);
      }

      // Se a resposta for OK, analisa a resposta JSON.
      const data = await response.json();
      // Verifica se a avaliação foi enviada com sucesso (data.bool).
      if (data.bool) {
        // Exibe mensagem de sucesso.
        reviewRes.textContent = "Avaliação enviada com sucesso!";
        reviewRes.classList.add("text-success");

        // Seleciona o contêiner de avaliações.
        const reviewsContainer = document.querySelector(".comment-container");
        // Verifica se o contêiner de avaliações existe.
        if (reviewsContainer) {
          // Cria um novo elemento div para a nova avaliação.
          const newReview = document.createElement("div");
          const rating = data.context.rating;

          // Gera as estrelas com base na classificação.
          let starsHTML = "";
          for (let i = 1; i <= 5; i++) {
            starsHTML += `<i class="fas fa-star ${i <= rating ? "text-warning" : "text-secondary"}"></i>`;
          }

          // Define as classes CSS e o conteúdo HTML do novo elemento de avaliação.
          newReview.className =
            "single-comment justify-content-between d-flex mb-30";
          newReview.innerHTML = `
                      <div class="user justify-content-between d-flex">
                        <div class="thumb text-center">
                          <img src="${data.context.user_image || "https://www.tenforums.com/geek/gars/images/2/types/thumb_15951118880user.png"}" alt="" />
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
                      <div>
                    `;
          // Adiciona a nova avaliação ao início do contêiner de avaliações.
          reviewsContainer.prepend(newReview);

          // Seleciona o elemento para exibir a média das avaliações e atualiza seu conteúdo.
          const averageRating = document.querySelector(".d-flex > h6");
          if (averageRating) {
            averageRating.textContent = `${data.media_aval.average_rating.toFixed(1)} de 5,0`;
          } else {
            console.error(
              "Error: Element with class 'd-flex > h6' not found. Check your HTML.",
            );
          }
        } else {
          console.error(
            "Error: Element with class 'comment-container' not found. Check your HTML.",
          );
        }
        // Limpa o formulário após o envio da avaliação.
        commentForm.reset();
      } else {
        // Exibe mensagem de erro caso a avaliação não tenha sido enviada.
        reviewRes.textContent =
          "Erro ao enviar a avaliação. Por favor, tente novamente.";
        reviewRes.classList.add("text-danger");
        console.error("Erro:", data.errors);
      }
    } catch (error) {
      // Trata erros ocorridos durante a requisição.
      reviewRes.textContent = `Erro: ${error.message}`;
      reviewRes.classList.add("text-danger");
      console.error("Erro:", error);
    }
  });
});

$(document).ready(function () {
  $(".filter-checkbox").on("click", function () {
    console.log("Um checkbox foi selecionado");

    let filter_object = {};

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
});
