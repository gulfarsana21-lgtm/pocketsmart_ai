async function parseError(response) {
    try {
        const data = await response.json();
        if (typeof data.detail === "string") return data.detail;
        if (Array.isArray(data.detail)) {
            return data.detail.map(item => item.msg || "Invalid input").join(", ");
        }
        return "Request failed.";
    } catch {
        return "Request failed.";
    }
}

function showMessage(element, text, type = "") {
    if (!element) return;
    element.textContent = text;
    element.className = "form-message";
    if (type) element.classList.add(type);
}

function setButtonLoading(button, loading) {
    if (!button) return;
    if (loading) {
        button.dataset.originalText = button.textContent;
        button.disabled = true;
        button.textContent = "Please wait...";
    } else {
        button.disabled = false;
        button.textContent = button.dataset.originalText || "Submit";
    }
}

function afterAuth() {
    const params = new URLSearchParams(window.location.search);
    const next = params.get("next");
    if (next && next.startsWith("/")) {
        window.location.href = next;
        return;
    }
    window.location.href = "/dashboard";
}

function setupAuthForm(formId, endpoint) {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener("submit", async event => {
        event.preventDefault();

        const message = document.getElementById("authMessage");
        const button = form.querySelector("button[type='submit']");
        showMessage(message, "Working...");
        setButtonLoading(button, true);

        try {
            const body = Object.fromEntries(new FormData(form).entries());
            const response = await fetch(endpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "same-origin",
                body: JSON.stringify(body),
            });

            if (!response.ok) throw new Error(await parseError(response));
            afterAuth();
        } catch (error) {
            showMessage(message, error.message, "error");
        } finally {
            setButtonLoading(button, false);
        }
    });
}

async function logout() {
    try {
        await fetch("/api/auth/logout", {
            method: "POST",
            credentials: "same-origin",
        });
    } finally {
        window.location.href = "/";
    }
}

async function loadSessionStats() {
    try {
        const response = await fetch("/api/session-data", {
            credentials: "same-origin",
        });
        if (!response.ok) return;

        const data = await response.json();
        const counts = data.planner_counts || {};

        document.getElementById("totalPlans").textContent = data.total_recommendations ?? 0;
        document.getElementById("homePlans").textContent = counts.home ?? 0;
        document.getElementById("partyPlans").textContent = counts.party ?? 0;
        document.getElementById("jewelryPlans").textContent = counts.jewelry ?? 0;
    } catch {
        // Counters are non-critical.
    }
}

async function deleteHistory(historyId) {
    if (!window.confirm("Delete this saved recommendation?")) return;

    const response = await fetch(`/api/history/${historyId}`, {
        method: "DELETE",
        credentials: "same-origin",
    });

    if (!response.ok) {
        window.alert(await parseError(response));
        return;
    }

    window.location.reload();
}

async function setupPlannerForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return;

    const planner = form.dataset.planner;
    const message = document.getElementById("plannerMessage");
    const button = form.querySelector("button[type='submit']");

    form.addEventListener("submit", async event => {
        event.preventDefault();
        showMessage(message, "Building your recommendation...");
        setButtonLoading(button, true);

        try {
            let body;
            const headers = {};

            if (planner === "jewelry") {
                body = new FormData(form);
            } else {
                const raw = Object.fromEntries(new FormData(form).entries());

                if (planner === "home") {
                    body = JSON.stringify({
                        budget: Number(raw.budget),
                        rooms: raw.rooms.split(",").map(v => v.trim()).filter(Boolean),
                        style: raw.style,
                        city: raw.city,
                        notes: raw.notes || "",
                    });
                } else {
                    body = JSON.stringify({
                        budget: Number(raw.budget),
                        guests: Number(raw.guests),
                        event_type: raw.event_type,
                        venue: raw.venue || "",
                        city: raw.city,
                        notes: raw.notes || "",
                    });
                }

                headers["Content-Type"] = "application/json";
            }

            const response = await fetch(`/api/planners/${planner}`, {
                method: "POST",
                headers,
                credentials: "same-origin",
                body,
            });

            if (response.status === 401) {
                window.location.href = `/login?next=/planner/${planner}`;
                return;
            }

            if (!response.ok) throw new Error(await parseError(response));

            const result = await response.json();
            if (!result.history_id) {
                throw new Error("No history ID was returned by the server.");
            }

            window.location.href = `/recommendations/${result.history_id}`;
        } catch (error) {
            showMessage(message, error.message, "error");
        } finally {
            setButtonLoading(button, false);
        }
    });
}
