<#import "template.ftl" as layout>
    <div class="top-content">
        **FOR DEMONSTRATION PURPOSES ONLY, ALL DATA IS UNCLASSIFIED** TS//SCI2//NOFORN
    </div>
    <nav class="navbar">
        <div class="logo-container">
            <img class="logo1" src="${url.resourcesPath}/img/dig_logo.png" />
            <img class="logo2" src="${url.resourcesPath}/img/B2_Logo.svg" />
        </div>
        <div class="nav-links-container">
            <ul class="nav-link">
                <li class="nav-link-item">Home</li>
                <li class="nav-link-item">Records</li>
                <li class="nav-link-item">Findata</li>
            </ul>
        </div>
    </nav>

    <div class="bg-container">
        <img class="bg1" src="${url.resourcesPath}/img/path_1.svg" />
        <img class="bg2" src="${url.resourcesPath}/img/stock_1.png" />
    </div>

    <@layout.registrationLayout displayMessage=!messagesPerField.existsError('username','password')
        displayInfo=realm.password && realm.registrationAllowed && !registrationDisabled??; section>
        <#if section="header">
            ${msg("loginAccountTitle")}
            <#elseif section="form">
                <div id="kc-form">
                    <div id="kc-form-wrapper">
                        <#if realm.password>
                            <form id="kc-form-login" onsubmit="login.disabled = true; return true;"
                                action="${url.loginAction}" method="post">
                                <div class="${properties.kcFormGroupClass!}">
                                    <label for="username" class="${properties.kcLabelClass!}">
                                        <#if !realm.loginWithEmailAllowed>${msg("username")}<#elseif
                                                !realm.registrationEmailAsUsername>${msg("usernameOrEmail")}<#else>
                                                    ${msg("email")}</#if>
                                    </label>

                                    <#if usernameEditDisabled??>
                                        <input tabindex="1" id="username" class="${properties.kcInputClass!}"
                                            name="username" value="${(login.username!'')}" type="text" disabled />
                                        <#else>
                                            <input tabindex="1" id="username" class="${properties.kcInputClass!}"
                                                name="username" value="${(login.username!'')}" type="text" autofocus
                                                autocomplete="off"
                                                aria-invalid="<#if messagesPerField.existsError('username','password')>true</#if>" />

                                            <#if messagesPerField.existsError('username','password')>
                                                <span id="input-error" class="${properties.kcInputErrorMessageClass!}"
                                                    aria-live="polite">
                                                    ${kcSanitize(messagesPerField.getFirstError('username','password'))?no_esc}
                                                </span>
                                            </#if>
                                    </#if>
                                </div>

                                <div class="${properties.kcFormGroupClass!}">
                                    <label for="password" class="${properties.kcLabelClass!}">${msg("password")}</label>

                                    <input tabindex="2" id="password" class="${properties.kcInputClass!}"
                                        name="password" type="password" autocomplete="off"
                                        aria-invalid="<#if messagesPerField.existsError('username','password')>true</#if>" />
                                </div>

                                <div class="${properties.kcFormGroupClass!} ${properties.kcFormSettingClass!}">
                                    <div id="kc-form-options">
                                        <#if realm.rememberMe && !usernameEditDisabled??>
                                            <div class="checkbox">
                                                <label>
                                                    <#if login.rememberMe??>
                                                        <input tabindex="3" id="rememberMe" name="rememberMe"
                                                            type="checkbox" checked> ${msg("rememberMe")}
                                                        <#else>
                                                            <input tabindex="3" id="rememberMe" name="rememberMe"
                                                                type="checkbox"> ${msg("rememberMe")}
                                                    </#if>
                                                </label>
                                            </div>
                                        </#if>
                                    </div>
                                    <div class="${properties.kcFormOptionsWrapperClass!}">
                                        <#if realm.resetPasswordAllowed>
                                            <span><a tabindex="5"
                                                    href="${url.loginResetCredentialsUrl}">${msg("doForgotPassword")}</a></span>
                                        </#if>
                                    </div>

                                </div>

                                <div id="kc-form-buttons" class="${properties.kcFormGroupClass!}">
                                    <input type="hidden" id="id-hidden-input" name="credentialId" <#if
                                        auth.selectedCredential?has_content>value="${auth.selectedCredential}"
                        </#if>/>
                        <input tabindex="4"
                            class="${properties.kcButtonClass!} ${properties.kcButtonPrimaryClass!} ${properties.kcButtonBlockClass!} ${properties.kcButtonLargeClass!}"
                            name="login" id="kc-login" type="submit" value="${msg("Sign In")}" />
                    </div>
                    </form>
        </#if>
        </div>

        <#if realm.password && social.providers??>
            <div id="kc-social-providers" class="${properties.kcFormSocialAccountSectionClass!}">
                <hr />
                <h4>${msg("identity-provider-login-label")}</h4>

                <ul
                    class="${properties.kcFormSocialAccountListClass!} <#if social.providers?size gt 3>${properties.kcFormSocialAccountListGridClass!}</#if>">
                    <#list social.providers as p>
                        <a id="social-${p.alias}"
                            class="${properties.kcFormSocialAccountListButtonClass!} <#if social.providers?size gt 3>${properties.kcFormSocialAccountGridItem!}</#if>"
                            type="button" href="${p.loginUrl}">
                            <#if p.iconClasses?has_content>
                                <i class="${properties.kcCommonLogoIdP!} ${p.iconClasses!}" aria-hidden="true"></i>
                                <span
                                    class="${properties.kcFormSocialAccountNameClass!} kc-social-icon-text">${p.displayName!}</span>
                                <#else>
                                    <span class="${properties.kcFormSocialAccountNameClass!}">${p.displayName!}</span>
                            </#if>
                        </a>
                    </#list>
                </ul>
            </div>
        </#if>

        </div>
        <#elseif section="info">
            <#if realm.password && realm.registrationAllowed && !registrationDisabled??>
                <div id="kc-registration-container">
                    <div id="kc-registration">
                        <span>${msg("noAccount")} <a tabindex="6"
                                href="${url.registrationUrl}">${msg("doRegister")}</a></span>
                    </div>
                </div>
            </#if>
            </#if>

    </@layout.registrationLayout>

    <div class="footer-container">
        <div class="footer-inner-container">
            <div class="footer-logo-container">
                <img src="${url.resourcesPath}/img/dia_symbol_trans1002x.png" class="footer-logo " />
            </div>
            <div class="footer-links-container">
                <ul>
                    <li><a href-"#" class="footer-link">Link Disclaimer</a></li>
                    <li><a href-"#" class="footer-link">Web Policy</a></li>
                    <li><a href-"#" class="footer-link">No FEAR Act</a></li>
                </ul>
                <ul>
                    <li><a href-"#" class="footer-link">DIA Inspector General</a></li>
                    <li><a href-"#" class="footer-link">DIA Status/OPM.gov</a></li>
                    <li><a href-"#" class="footer-link">Accessibility/Section 508</a></li>
                </ul>
                <ul>
                    <li><a href-"#" class="footer-link">Equal Opportunities & Diversity</a></li>
                    <li><a href-"#" class="footer-link">Employee Resources</a></li>
                    <li><a href-"#" class="footer-link">Web Policy & Security</a></li>
                </ul>
                <ul>
                    <li><a href-"#" class="footer-link">Defense.gov</a></li>
                    <li><a href-"#" class="footer-link">Intel.gov</a></li>
                    <li><a href-"#" class="footer-link">FOIA</a></li>
                </ul>
                <ul>
                    <li><a href-"#" class="footer-link">Contact Us</a></li>
                    <li><a href-"#" class="footer-link">Open GOV</a></li>
                    <li><a href-"#" class="footer-link">SiteMap</a></li>
                </ul>
            </div>
        </div>
        <div>
            <h6 class="footer-bot-text">
                <i>COMMITTED TO EXCELLENCE IN DEFENSE OF THE NATION</i>
            </h6>
        </div>
    </div>

    <div class="bot-content">
        **FOR DEMONSTRATION PURPOSES ONLY, ALL DATA IS UNCLASSIFIED** TS//SCI2//NOFORN
    </div>