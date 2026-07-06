// hashing funciton
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