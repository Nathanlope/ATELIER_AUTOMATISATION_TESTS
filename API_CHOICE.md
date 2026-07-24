# API Choice

- Étudiant : Nathan Lopes
- API choisie : ipify
- URL base : https://api.ipify.org
- Documentation officielle / README : https://www.ipify.org
- Auth : None
- Endpoints testés :
  * GET /?format=json
  * GET / (sans format, retourne du texte brut)
- Hypothèses de contrat (champs attendus, types, codes) :
  * GET /?format=json → 200, Content-Type: application/json, body {"ip": "<string>"}
  * GET / (sans param) → 200, text/plain, corps = adresse IP brute
- Limites / rate limiting connu : non documenté officiellement, usage raisonnable recommandé
- Risques (instabilité, downtime, CORS, etc.) : service tiers gratuit, pas de SLA garanti
