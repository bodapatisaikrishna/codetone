# Answer key — userinfo.go (15 seeded violations)
G1 dot import `. "fmt"`
G2 `MAX_RETRIES` — constants should be MixedCaps (`MaxRetries`)
G3 `UserInfo` in package `user` — stutter (`user.UserInfo`), and `NewUserInfo`
G4 `context.Context` stored in a struct
G5 `userId` — initialism should be `userID`
G6 `Url` — initialism should be `URL`
G7 `user_count` — underscores in name
G8 receiver named `this` (use short name like `u`)
G9 `GetUserId` — no `Get` prefix, and `Id` → `ID`
G10 ctx not the first parameter in `NewUserInfo(id, ctx)`
G11 `interface{}` — use `any`
G12 ignored error `f, _ := os.Open`
G13 error string capitalized and ends with punctuation
G14 `else` after return — indent error flow
G15 `panic` for normal error handling (and `Must` naming misuse)
G16 exported functions/types/consts missing doc comments; no package comment
G17 error swallowed in Lookup (returns "" — in-band error)
G18 gofmt: struct field alignment not gofmt'd
(18 items; score = found / 18)
