package clearance_policy

default allow = false

allow {
    input.request.method == "GET"
    input.request.path = ["graphql"]
    user_clearance := input.request.user.roles[_].name
    data.models.Record.clearance_level[user_clearance] >= data.models.Record.clearance_level[input.request.record.clearance]
}
