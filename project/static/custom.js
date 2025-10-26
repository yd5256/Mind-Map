const starsContainer = document.getElementById("stars");
const starCount = 150;

for (let i = 0; i < starCount; i++) {
  const star = document.createElement("div");
  star.className = "star";

  // Add color variety
  const colorRand = Math.random();
  if (colorRand < 0.1) {
    star.style.background = "#ffd700";
    star.style.boxShadow = "0 0 4px #ffd700";
  } else if (colorRand < 0.2) {
    star.style.background = "#ff69b4";
    star.style.boxShadow = "0 0 4px #ff69b4";
  } else if (colorRand < 0.3) {
    star.style.background = "#da70ff";
    star.style.boxShadow = "0 0 4px #da70ff";
  }

  const size = Math.random() * 3 + 1;
  star.style.width = `${size}px`;
  star.style.height = `${size}px`;

  star.style.left = `${Math.random() * 100}%`;
  star.style.top = `${Math.random() * 100}%`;

  star.style.animationDuration = `${Math.random() * 3 + 2}s`;
  star.style.animationDelay = `${Math.random() * 3}s`;

  starsContainer.appendChild(star);
}

// Map form helper: multi-stage client-side generation
document.addEventListener('DOMContentLoaded', () => {
  // find the map form (action contains /map)
  const mapForm = Array.from(document.forms).find(f => f.action && f.action.includes('/map'));
  if (!mapForm) return;

  const submitButton = mapForm.querySelector('button[type="submit"], input[type="submit"]');
  let injectedSubtopics = false;
  let injectedChildren = false;

  function setSubmitLabel(text) {
    if (!submitButton) return;
    if (submitButton.tagName.toLowerCase() === 'input') submitButton.value = text;
    else submitButton.textContent = text;
  }

  mapForm.addEventListener('submit', (e) => {
    // First click: inject 3 top-level subtopic inputs
    if (!injectedSubtopics) {
      e.preventDefault();
      injectedSubtopics = true;

      const container = document.createElement('div');
      container.className = 'generated-subtopics';
      const heading = document.createElement('h4');
      heading.textContent = 'Enter 3 subtopics';
      container.appendChild(heading);

      for (let i = 0; i < 3; i++) {
        const fg = document.createElement('div');
        fg.className = 'form-group';

        const label = document.createElement('label');
        label.setAttribute('for', `subtopic_${i}`);
        label.textContent = `Subtopic ${i + 1}`;

        const input = document.createElement('input');
        input.type = 'text';
        input.name = `subtopic_${i}`;
        input.id = `subtopic_${i}`;
        input.className = 'form-input';
        input.placeholder = `Subtopic ${i + 1}`;

        fg.appendChild(label);
        fg.appendChild(input);
        container.appendChild(fg);
      }

      if (submitButton) mapForm.insertBefore(container, submitButton);
      else mapForm.appendChild(container);
      setSubmitLabel('Add details for subtopics');
      return;
    }

    // Second click: inject 3 child inputs per subtopic if not already injected
    if (injectedSubtopics && !injectedChildren) {
      e.preventDefault();
      injectedChildren = true;

      // find the top-level subtopic inputs (names like subtopic_0)
      const topSubtopics = Array.from(mapForm.querySelectorAll('input[name^="subtopic_"]'))
        .filter(inp => !inp.name.includes('_child_'));

      const childContainer = document.createElement('div');
      childContainer.className = 'generated-children';
      const heading = document.createElement('h4');
      heading.textContent = 'Enter 3 details for each subtopic';
      childContainer.appendChild(heading);

      topSubtopics.forEach((inp, idx) => {
        const group = document.createElement('div');
        group.className = 'subtopic-group';
        const title = document.createElement('h5');
        title.textContent = `Details for: ${inp.value || 'Subtopic ' + (idx+1)}`;
        group.appendChild(title);

        for (let j = 0; j < 3; j++) {
          const fg = document.createElement('div');
          fg.className = 'form-group';
          const label = document.createElement('label');
          label.setAttribute('for', `${inp.name}_child_${j}`);
          label.textContent = `Detail ${j + 1}`;

          const childInput = document.createElement('input');
          childInput.type = 'text';
          childInput.name = `${inp.name}_child_${j}`;
          childInput.id = `${inp.name}_child_${j}`;
          childInput.className = 'form-input';
          childInput.placeholder = `Detail ${j + 1} for ${inp.value || 'subtopic'}`;

          fg.appendChild(label);
          fg.appendChild(childInput);
          group.appendChild(fg);
        }

        childContainer.appendChild(group);
      });

      if (submitButton) mapForm.insertBefore(childContainer, submitButton);
      else mapForm.appendChild(childContainer);
      setSubmitLabel('Submit All');
      return;
    }

    // If both injected, allow submit to proceed and server will receive all fields
  });
});
