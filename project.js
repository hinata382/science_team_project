document.addEventListener("DOMContentLoaded", () => {

  function searchElement() {
    const symbol = document.getElementById("symbolInput").value;
    const group = document.getElementById("groupInput").value;
    const period = document.getElementById("periodInput").value;

    const query = new URLSearchParams({ symbol, group, period });

    fetch(`/api/search?${query}`)
      .then(res => {
        if (!res.ok) throw new Error("서버 응답 오류");
        return res.json();
      })
      .then(data => {
        const resultBox = document.getElementById("result");
        if (data.error) {
          resultBox.textContent = "❌ " + data.error;
        } else if (Array.isArray(data)) {
          resultBox.textContent = data
            .map(e => `${e.symbol} (${e.name}) - ${e.group}족, ${e.period}주기`)
            .join("\n");
        } else {
          resultBox.textContent = `${data.symbol} (${data.name}) - ${data.group}족, ${data.period}주기`;
        }
      })
      .catch(err => {
        document.getElementById("result").textContent = "⚠️ 검색 중 오류가 발생했습니다.";
      });
  }

  const searchBtn = document.getElementById("searchBtn");
  if (searchBtn) {
    searchBtn.addEventListener("click", searchElement);
  }

  const tooltip = document.getElementById("tooltip");
  document.querySelectorAll("td").forEach(cell => {
    const symbol = cell.textContent.split('\n')[0].trim();
    if (!symbol) return;

    cell.addEventListener("mouseenter", async (e) => {
      try {
        const res = await fetch(`/api/search?symbol=${symbol}`);
        if (!res.ok) throw new Error();
        const data = await res.json();

        if (!data.error) {
          tooltip.textContent = `${data.symbol} (${data.name}) - ${data.group}족, ${data.period}주기`;
        } else {
          tooltip.textContent = data.error;
        }
      } catch {
        tooltip.textContent = "정보 없음";
      }

      tooltip.style.visibility = "visible";
      tooltip.style.opacity = "1";
      moveTooltip(e);
    });

    cell.addEventListener("mousemove", moveTooltip);

    cell.addEventListener("mouseleave", () => {
      tooltip.style.visibility = "hidden";
      tooltip.style.opacity = "0";
    });
  });

  function moveTooltip(e) {
    tooltip.style.left = e.clientX + window.scrollX + 10 + "px";
    tooltip.style.top = e.clientY + window.scrollY + 10 + "px";
  }
});
