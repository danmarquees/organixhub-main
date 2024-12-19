document.addEventListener("DOMContentLoaded", () => {
  const commentForm = document.getElementById("commentForm");
  const reviewRes = document.getElementById("review-res");

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
          let errorMessages = "";
          for (const field in data.errors) {
            errorMessages += `${field}: ${data.errors[field][0]}\n`;
          }
          throw new Error(errorMessages);
        }
        throw new Error(`Erro HTTP ${response.status}`);
      }

      const data = await response.json();
      if (data.bool) {
        reviewRes.textContent = "Avaliação enviada com sucesso!";
        reviewRes.classList.add("text-success");

        const reviewsContainer = document.querySelector(".comment-container");
        if (reviewsContainer) {
          const newReview = document.createElement("div");
          const rating = data.context.rating;
          let starsHTML = "";

          for (let i = 1; i <= rating; i++) {
            starsHTML += `<i class="fas fa-star"></i>`;
          }

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
                  <div class="product-rate d-inline-block">
                    ${starsHTML}
                  </div>
                </div>
                <p class="mb-10">${data.context.review}</p>
              </div>
            </div>
          `;
          reviewsContainer.prepend(newReview);

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
        commentForm.reset();
      } else {
        reviewRes.textContent =
          "Erro ao enviar a avaliação. Por favor, tente novamente.";
        reviewRes.classList.add("text-danger");
        console.error("Erro:", data.errors);
      }
    } catch (error) {
      reviewRes.textContent = `Erro: ${error.message}`;
      reviewRes.classList.add("text-danger");
      console.error("Erro:", error);
    }
  });
});
