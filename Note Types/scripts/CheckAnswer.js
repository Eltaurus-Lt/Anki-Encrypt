async function sha256withSalt(text, saltString) {
	const encoder = new TextEncoder();
	const salt = saltString ? Uint8Array.from(saltString.match(/.{2}/g).map(byte => parseInt(byte, 16))) : new Uint8Array(0);
	const data = encoder.encode(text);
    
	const salted_data = new Uint8Array(salt.length + data.length);
	salted_data.set(salt);
	salted_data.set(data, salt.length);
    
	const hashBuffer = await crypto.subtle.digest('SHA-256', salted_data);
	const hashArray = Array.from(new Uint8Array(hashBuffer));
    
	return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

typeAnsL = document.getElementById("typeans");
typedLs = typeAnsL.querySelectorAll("span:is(.typeGood,.typeBad):not(br ~ span)");
correctLs = typeAnsL.querySelectorAll("span:is(br ~ br ~ span)");

typedAns = [...typedLs].map(L => L.textContent).join('');
saltedHash = [...correctLs].map(L => L.textContent).join('');
correctHash = saltedHash.slice(-64);
saltString = saltedHash.slice(0, -64);

sha256withSalt(typedAns, saltString).then((typedHash) => {
	const cardL = document.querySelector(".card");
	if (typedHash === correctHash) {
		cardL.classList.add('correct');
		typeAnsL.innerHTML = `✅`; \\${typedAns}
	} else {
		cardL.classList.add('wrong');
		typeAnsL.innerHTML = `❌`; \\${typedAns}
	}
});