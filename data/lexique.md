

> `Mois`: il s’agit du mois pour lequel l’utilisateur souhaite visualiser les données

>     
>`Statut`:  il s’agit du statut du PDV calculé à la dernière date du mois pour les mois complets, ou à la dernière date disponible pour les mois incomplets.
Le `Statut global` est calculé sur l’activité globale du PDV, tandis que le `Statut Cash in/Cash out` est calculé sur les activités `Cash In` et `Cash Out` du PDV.
- `Actif` si la dernière transaction du PDV date de `0` à `20` jours
- `Futur inactif` si la dernière transaction du PDV date de `21` à `29` jours
- `Inatif récent` si la dernière transaction du PDV date de `30` à `89` jours
- `Inactif âgé` si la dernière transaction du PDV date de plus de `89` jours



>`Performance PDV`: Il s’agit d’une catégorisation des PDVs en fonction des montants des commissions réalisées au cours du mois.  
- `Zero` si le montant des commissions est égal à `0`
- `Low` si le montant des commisions est compris entre `0` et `1 000`
- `Medium` si le montant des commisions est compris entre `1 000` et `10 000`
- `High` si le montant des commissions est compris entre `10 000` et `50 000`
- `Super High` si le montant des commissions est supérieur à `50 000`

>`Localisation`:  elle est définie en priorité par le dernier relevé `GPS` du PDV remonté à travers les visites terrain. Le PDV est ensuite placé dans le zoning (`SITE`, `ZONE`, `DACR`, `SECTEUR`) à travers le site de couverture Orange le plus proche de sa position. Si aucun relevé GPS n’est disponible, la localisation système du MSISDN du PDV est conservée. La localisation système est remplacée dès qu’un relevé GPS est disponible.  

>`Impact des visites`:  Il s’agit de l’impact constaté sur le statut des PDV visités   
- `Jamais visité`: PDV jamais visité, n’apparait pas dans l’historique des visites  
- `Non visité`: PDV au moins une fois visité, mais n’ayant pas été visité au cours du mois sélectionné  
- `N'a pas réagi`: PDV visité au cours du mois sélectionné, mais dont le statut n’a pas évolué par rapport au mois précédent (exemple: Inactif récent au mois sélectionné, Inactif récent au mois précédent)  
- `A maintenu son statut`: PDV visité au cours du mois sélectionné et ayant conservé son statut du mois précédent (exemple: Actif au mois sélectionné, Actif au mois précédent)  
- `A réagi`: PDV visité au cours du mois sélectionné, et ayant amélioré son statut par rapport au mois précédent (exemple: Actif au mois sélectionné, Inactif récent au mois précédent)  
- `Nouveau PDV visité`: PDV visité et qui apparait pour la première fois dans la base  
