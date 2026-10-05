let state = {goal:"", tasks:[]};

function fillExample(){
  document.getElementById("goal").value = "I have a hackathon next Friday. Get me ready.";
}

async function createPlan(){
  const goal = document.getElementById("goal").value.trim();
  if(!goal) return toast("Please enter a goal first.");
  const btn = document.getElementById("planBtn");
  btn.disabled = true; btn.textContent = "Creating workflow...";
  const res = await fetch("/api/plan",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({goal})});
  const data = await res.json();
  btn.disabled = false; btn.textContent = "✦ Create workflow";
  if(data.error) return toast(data.error);
  state.goal = data.goal; state.tasks = data.tasks;
  document.getElementById("workspace").classList.remove("hidden");
  document.getElementById("goalTitle").textContent = data.goal;
  renderTasks();
  document.getElementById("workspace").scrollIntoView({behavior:"smooth"});
  toast("Workflow created.");
}

function renderTasks(){
  const box = document.getElementById("tasks");
  box.innerHTML = state.tasks.map((t,i)=>`
    <div class="task">
      <div class="check ${t.status==="completed"?"done":""}" onclick="completeTask(${i})">${t.status==="completed"?"✓":""}</div>
      <div><div class="task-title">${t.title}</div><div class="task-meta">${t.category}</div></div>
      <div class="badge">${t.priority}</div>
    </div>`).join("");
  const done = state.tasks.filter(t=>t.status==="completed").length;
  const pct = state.tasks.length ? Math.round(done/state.tasks.length*100) : 0;
  document.getElementById("progressText").textContent = pct+"% complete";
}

function completeTask(i){
  state.tasks[i].status = state.tasks[i].status==="completed" ? "pending" : "completed";
  renderTasks();
}

function showReplan(){document.getElementById("replanModal").classList.remove("hidden")}
function hideReplan(){document.getElementById("replanModal").classList.add("hidden")}

async function replan(){
  const constraint = document.getElementById("constraint").value.trim();
  if(!constraint) return toast("Tell FlowPilot what changed.");
  const res = await fetch("/api/replan",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({goal:state.goal,constraint})});
  const data = await res.json();
  state.tasks = data.tasks;
  renderTasks();
  hideReplan();
  document.getElementById("constraint").value = "";
  toast("Workflow adapted to the new constraint.");
}

function toast(msg){
  const el=document.getElementById("toast"); el.textContent=msg; el.style.display="block";
  clearTimeout(window._toast); window._toast=setTimeout(()=>el.style.display="none",2600);
}
