
package rowfilter

default allow = {"allow": false, "predicate": ""}

allow = resp {
  user := input.user
  tables := input.tables
  users[user]
  region := users[user].region
  preds := [sprintf("%s.region = '%s'", [t, region]) | t := tables[_]]
  resp := {"allow": true, "predicate": concat(" AND ", preds)}
}

users = {
  "alice": {"region": "NA"},
  "bob":   {"region": "EU"}
}
