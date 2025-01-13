// Función para generar un carácter aleatorio (glitch effect)
function randomChar() {
	const chars =
		"!@#$%^&*()_+=-[]{}|;:,.<>?~abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
	return chars[Math.floor(Math.random() * chars.length)];
}

// Función para aplicar el glitch en el texto
function glitchEffect(text) {
	const glitchChance = 0.05;
	return text
		.split("")
		.map(char => (char === "\n" ? char : Math.random() < glitchChance ? randomChar() : char))
		.join("");
}

// Función para escribir una frase
function writePhrase(phrase, element, callback, delay = 150) {
	let charIndex = 0;

	function type() {
		const displayedText = glitchEffect(phrase.substring(0, charIndex));
		element.innerHTML = displayedText;
		charIndex++;

		if (charIndex <= phrase.length) {
			setTimeout(type, delay);
		} else if (callback) {
			setTimeout(callback, 1000);
		}
	}

	type();
}

// Función para borrar una frase
function deletePhrase(phrase, element, callback, delay = 75) {
	let charIndex = phrase.length;

	function erase() {
		const displayedText = glitchEffect(phrase.substring(0, charIndex));
		element.innerHTML = displayedText;
		charIndex--;

		if (charIndex >= 0) {
			setTimeout(erase, delay);
		} else if (callback) {
			setTimeout(callback, 500);
		}
	}

	erase();
}

const outputElement = document.querySelector(".output");

// Frases para animar
const phrases = [
	'Iniciando protocolo...\nCargando datos [#Lumino v2.3.5]\nConexión establecida: "Acceso autorizado"',
	"Proceso completado\nIniciando comunicaciones... \nVerificando acceso...\n¡Todo listo!",
];

let phraseIndex = 0;

// Controlador principal para alternar entre escribir y borrar
function animateText() {
	if (phraseIndex < phrases.length) {
		const currentPhrase = phrases[phraseIndex];

		writePhrase(currentPhrase, outputElement, () => {
			deletePhrase(currentPhrase, outputElement, () => {
				phraseIndex++;
				animateText(); // Llamada recursiva para la siguiente frase
			}, 15);
		}, 15);
	} else {
		addLinks();
	}
}

// Función para añadir enlaces después de la última frase
function addLinks() {
	// Crear elementos dinámicamente
	const p = document.createElement('p');
	const ul = document.createElement('ul');

	// Frase para el <p>
	const phrase = "¿Listo para comenzar? Haz clic en los enlaces:";

	// Crear los enlaces dentro de la lista
	const links = [
		{ href: '/signup', text: "Registrate" },
		{ href: '/login', text: "Inicia sesion" },
	];

	// Insertar el <p> en el DOM antes de animarlo
	outputElement.appendChild(p);

	// Aplicar glitch al texto del <p> y, cuando termine, añadir los enlaces
	writePhrase(phrase, p, () => {
		// Construir lista de enlaces después de terminar el texto
		links.forEach(link => {
			const li = document.createElement('li');
			const a = document.createElement('a');
			a.href = link.href;
			a.textContent = link.text;
			li.appendChild(a);
			ul.appendChild(li);
		});

		// Insertar la lista en el DOM
		outputElement.appendChild(ul);
	}, 30); // Velocidad de escritura
}


// Inicia la animación
animateText();