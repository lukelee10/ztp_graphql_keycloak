package policy
import future.keywords.every

default allow = false

allow_login {
    input.user.clearance == "TOPSECRET"
}
allow_login {
    input.user.clearance == "SECRET"
}
allow_login {
    input.user.clearance == "CONFIDENTIAL"
}
allow_login {
    input.user.clearance == "UNCLASSIFIED"
}

clearance_auth {
    input.user.clearance_level >= input.doc.classification
}



attribute_auth {
    input.doc.access_attributes == input.user.access_attributes[i]
}


