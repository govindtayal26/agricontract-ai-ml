/*
 * AgriContract - Main JavaScript
 * Django-based frontend
 *
 * Keeps:
 * - Navigation
 * - Mobile menu
 * - User dropdown
 * - Loading screen
 * - Animations
 * - Counters
 * - Login/Register UI
 * - Password visibility
 * - Toast notifications
 * - Language switching
 * - Weather API
 * - Crop disease detector API
 *
 * Removed:
 * - Mock crop data
 * - Mock contract data
 * - Fake authentication/localStorage
 * - Fake video calling
 * - Fake market analytics
 * - Fake chat responses
 * - Fake "coming soon" features
 * - Fake performance/demo code
 */

let currentLanguage = "en";

/* =========================================================
   TRANSLATIONS
   ========================================================= */

const translations = {
    en: {
        brand: "AgriContract",

        nav: {
            home: "Home",
            features: "Features",
            how_it_works: "How It Works",
            disease_detector: "Disease Detector",
            market_analytics: "Market Analytics",
            about: "About",
            dashboard: "Dashboard",
            profile: "Profile",
        },

        hero: {
            trusted_by: "Trusted by 10,000+ Farmers",
            title_1: "Assured Contract Farming System",
            title_2: "for Stable Market Access",
            description:
                "Connect farmers directly with buyers through secure contract farming. Guaranteed prices, reliable supply, and transparent transactions for everyone.",

            stats: {
                farmers: "Active Farmers",
                buyers: "Verified Buyers",
                contracts: "Contracts Completed",
            },

            join_farmer: "Join as Farmer",
            join_buyer: "Join as Buyer",

            floating: {
                growth: "Market Growth +25%",
                secure: "100% Secure",
                direct: "Direct Trading",
            },
        },

        features: {
            title: "Why Choose AgriContract?",
            subtitle: "Revolutionizing agriculture through technology and trust",

            secure: {
                title: "Secure Contracts",
                description:
                    "Legal binding contracts with guaranteed payments and delivery terms.",
            },

            direct: {
                title: "Direct Connection",
                description:
                    "No middlemen - farmers connect directly with buyers for better prices.",
            },

            insights: {
                title: "Market Insights",
                description:
                    "AI-powered crop price prediction and agricultural market intelligence.",
            },

            communication: {
                title: "Contract Chat",
                description:
                    "Communicate directly with buyers and farmers through secure contract chat.",
            },

            disease: {
                title: "Disease Detection",
                description:
                    "AI-powered crop disease detection using uploaded crop images.",
            },

            mobile: {
                title: "Mobile First",
                description:
                    "Easy-to-use responsive interface designed for farmers and buyers.",
            },

            learn_more: "Learn More",
        },

        auth: {
            login: "Login",
            get_started: "Get Started",
            logout: "Logout",
            welcome_back: "Welcome Back",
            create_account: "Create Your Account",

            email: "Email",
            password: "Password",
            full_name: "Full Name",
            phone: "Phone Number",
            address: "Address",
            role: "I am a",
            confirm_password: "Confirm Password",

            remember_me: "Remember me",
            forgot_password: "Forgot Password?",

            sign_in: "Sign In",
            sign_up: "Create Account",

            no_account: "Don't have an account?",
            have_account: "Already have an account?",

            farmer: "Farmer",
            buyer: "Buyer",
            select_role: "Select your role",

            farmer_option: "🌾 Farmer - I want to sell my crops",
            buyer_option: "🛒 Buyer - I want to buy crops",

            email_placeholder: "Enter your email",
            password_placeholder: "Enter your password",
            name_placeholder: "Enter your full name",
            phone_placeholder: "Enter your phone number",
            address_placeholder: "Enter your address",

            create_password: "Create a password",
            confirm_password_placeholder: "Confirm your password",

            terms_agreement:
                "I agree to the Terms of Service and Privacy Policy",
        },

        disease: {
            title: "Crop Disease Detection",
            upload_title: "Upload Crop Image",
            upload_description:
                "Upload an image of your crop for AI-powered disease detection",
            choose_image: "Choose Image",
            results_title: "Detection Results",
        },
    },

    hi: {
        brand: "एग्रीकॉन्ट्रैक्ट",

        nav: {
            home: "होम",
            features: "विशेषताएं",
            how_it_works: "यह कैसे काम करता है",
            disease_detector: "रोग डिटेक्टर",
            market_analytics: "बाजार विश्लेषण",
            about: "हमारे बारे में",
        },

        hero: {
            trusted_by: "10,000+ किसानों का भरोसा",
            title_1: "सुनिश्चित कॉन्ट्रैक्ट फार्मिंग सिस्टम",
            title_2: "स्थिर बाजार पहुंच के लिए",
            description:
                "सुरक्षित कॉन्ट्रैक्ट फार्मिंग के माध्यम से किसानों को सीधे खरीदारों से जोड़ें। गारंटीशुदा कीमतें और पारदर्शी लेनदेन।",
        },
    },
};


/* =========================================================
   INITIALIZATION
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    initializeApp();
});


function initializeApp() {
    showLoadingScreen();

    setTimeout(() => {
        hideLoadingScreen();

        initializeNavigation();
        initializeAnimations();
        initializeCounters();
        initializeForms();
        initializeLanguage();
        initializeWeather();
        initializeParticles();
        initializeScrollEffects();
    }, 800);
}


/* =========================================================
   LOADING SCREEN
   ========================================================= */

function showLoadingScreen() {
    const loadingScreen = document.getElementById("loading-screen");

    if (!loadingScreen) return;

    loadingScreen.classList.remove("hidden");
}


function hideLoadingScreen() {
    const loadingScreen = document.getElementById("loading-screen");

    if (!loadingScreen) return;

    loadingScreen.classList.add("hidden");

    setTimeout(() => {
        loadingScreen.style.display = "none";
    }, 500);
}


/* =========================================================
   NAVIGATION
   ========================================================= */

function initializeNavigation() {
    const navbar = document.getElementById("navbar");

    if (navbar) {
        window.addEventListener("scroll", () => {
            navbar.classList.toggle(
                "scrolled",
                window.scrollY > 50
            );
        });
    }

    document.addEventListener("click", (event) => {
        const navMenu = document.getElementById("nav-menu");
        const navToggle = document.querySelector(".nav-toggle");

        if (!navMenu || !navToggle) return;

        if (
            !navMenu.contains(event.target) &&
            !navToggle.contains(event.target)
        ) {
            navMenu.classList.remove("show");
            navToggle.classList.remove("active");
        }
    });
}


function toggleMobileMenu() {
    const navMenu = document.getElementById("nav-menu");
    const navToggle = document.querySelector(".nav-toggle");

    if (!navMenu || !navToggle) return;

    navMenu.classList.toggle("show");
    navToggle.classList.toggle("active");
}


function closeMobileMenu() {
    const navMenu = document.getElementById("nav-menu");
    const navToggle = document.querySelector(".nav-toggle");

    if (!navMenu || !navToggle) return;

    navMenu.classList.remove("show");
    navToggle.classList.remove("active");
}


function toggleUserMenu() {
    const dropdown = document.getElementById("user-dropdown");

    if (!dropdown) return;

    dropdown.classList.toggle("show");
}


function showPage(pageId) {
    const pages = document.querySelectorAll(".page");

    pages.forEach((page) => {
        page.classList.remove("active");
    });

    const targetPage = document.getElementById(`${pageId}-page`);

    if (targetPage) {
        targetPage.classList.add("active");
    }

    closeMobileMenu();
}


function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);

    if (!section) return;

    section.scrollIntoView({
        behavior: "smooth",
        block: "start",
    });

    closeMobileMenu();
}


/* =========================================================
   ANIMATIONS
   ========================================================= */

function initializeAnimations() {
    const animatedElements = document.querySelectorAll("[data-aos]");

    if (!animatedElements.length) return;

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("animate-in");
                    observer.unobserve(entry.target);
                }
            });
        },
        {
            threshold: 0.1,
            rootMargin: "0px 0px -50px 0px",
        }
    );

    animatedElements.forEach((element) => {
        observer.observe(element);
    });
}


/* =========================================================
   COUNTERS
   ========================================================= */

function initializeCounters() {
    const counters = document.querySelectorAll("[data-count]");

    if (!counters.length) return;

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;

                const counter = entry.target;
                const target = Number.parseInt(
                    counter.getAttribute("data-count"),
                    10
                );

                if (!Number.isNaN(target)) {
                    animateCounter(counter, target);
                }

                observer.unobserve(counter);
            });
        },
        {
            threshold: 0.1,
        }
    );

    counters.forEach((counter) => {
        observer.observe(counter);
    });
}


function animateCounter(element, target) {
    const duration = 1500;
    const startTime = performance.now();

    function update(currentTime) {
        const progress = Math.min(
            (currentTime - startTime) / duration,
            1
        );

        const value = Math.floor(progress * target);

        element.textContent = value.toLocaleString();

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}


/* =========================================================
   PARTICLES
   ========================================================= */

function initializeParticles() {
    const heroParticles =
        document.querySelector(".hero-particles");

    if (!heroParticles) return;

    /*
     * Keep this lightweight.
     * Only create particles if the container exists.
     */

    const particleCount = 15;

    for (let i = 0; i < particleCount; i++) {
        createParticle(heroParticles);
    }
}


function createParticle(container) {
    const particle = document.createElement("div");

    const size = Math.random() * 4 + 2;

    particle.style.position = "absolute";
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;
    particle.style.background =
        "rgba(255, 255, 255, 0.1)";
    particle.style.borderRadius = "50%";
    particle.style.left = `${Math.random() * 100}%`;
    particle.style.top = `${Math.random() * 100}%`;
    particle.style.animation =
        `particleFloat ${Math.random() * 10 + 10}s linear infinite`;
    particle.style.animationDelay =
        `${Math.random() * 10}s`;

    container.appendChild(particle);
}


/* =========================================================
   SCROLL EFFECTS
   ========================================================= */

function initializeScrollEffects() {
    const heroBackground =
        document.querySelector(".hero-background");

    if (!heroBackground) return;

    let ticking = false;

    window.addEventListener("scroll", () => {
        if (ticking) return;

        window.requestAnimationFrame(() => {
            const scrolled = window.pageYOffset;

            heroBackground.style.transform =
                `translateY(${scrolled * 0.5}px)`;

            ticking = false;
        });

        ticking = true;
    });
}


/* =========================================================
   FORMS
   ========================================================= */

function initializeForms() {
    const loginForm =
        document.getElementById("login-form");

    const registerForm =
        document.getElementById("register-form");

    const cropImageInput =
        document.getElementById("crop-image-input");


    if (loginForm) {
        loginForm.addEventListener(
            "submit",
            handleLogin
        );
    }


    if (registerForm) {
        registerForm.addEventListener(
            "submit",
            handleRegister
        );
    }


    if (cropImageInput) {
        cropImageInput.addEventListener(
            "change",
            handleImageUpload
        );
    }
}


/*
 * Login is handled by Django.
 * We only show a loading state.
 */

function handleLogin(event) {
    const form = event.target;

    const submitButton =
        form.querySelector(
            'button[type="submit"]'
        );

    if (!submitButton) return true;

    submitButton.innerHTML =
        '<i class="fas fa-spinner fa-spin"></i> Signing In...';

    submitButton.disabled = true;

    return true;
}


/*
 * Registration is handled by Django.
 * Validate password confirmation before submitting.
 */

function handleRegister(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    const password =
        formData.get("password");

    const confirmPassword =
        formData.get("confirm_password");


    if (password !== confirmPassword) {
        showToast(
            "Registration Failed",
            "Passwords do not match.",
            "error"
        );

        return;
    }


    const submitButton =
        form.querySelector(
            'button[type="submit"]'
        );

    if (submitButton) {
        submitButton.innerHTML =
            '<i class="fas fa-spinner fa-spin"></i> Creating Account...';

        submitButton.disabled = true;
    }

    form.submit();
}


/* =========================================================
   PASSWORD
   ========================================================= */

function togglePassword(inputId) {
    const input =
        document.getElementById(inputId);

    if (!input) return;

    const button =
        input.nextElementSibling;

    if (!button) return;

    const icon =
        button.querySelector("i");

    if (!icon) return;


    if (input.type === "password") {
        input.type = "text";
        icon.className =
            "fas fa-eye-slash";
    } else {
        input.type = "password";
        icon.className =
            "fas fa-eye";
    }
}


/* =========================================================
   DEMO CREDENTIAL HELP
   ========================================================= */

function copyCredentials(email, password) {
    const emailInput =
        document.getElementById("login-email");

    const passwordInput =
        document.getElementById("login-password");

    if (emailInput) {
        emailInput.value = email;
    }

    if (passwordInput) {
        passwordInput.value = password;
    }

    showToast(
        "Credentials Filled",
        "Demo credentials have been filled.",
        "info"
    );
}


/* =========================================================
   DJANGO AUTHENTICATION
   ========================================================= */

/*
 * IMPORTANT:
 *
 * Django controls authentication.
 * Do NOT use localStorage for login state.
 */

function checkAuthStatus() {
    console.log(
        "AgriContract: Authentication handled by Django."
    );
}


/* =========================================================
   MODALS
   ========================================================= */

function showModal(modalId) {
    const modal =
        document.getElementById(modalId);

    if (!modal) return;

    modal.classList.add("show");

    document.body.style.overflow = "hidden";

    const firstInput =
        modal.querySelector(
            "input, select, textarea"
        );

    if (firstInput) {
        setTimeout(() => {
            firstInput.focus();
        }, 100);
    }
}


function closeModal(modalId) {
    const modal =
        document.getElementById(modalId);

    if (!modal) return;

    modal.classList.remove("show");

    document.body.style.overflow = "";
}


function showLogin() {
    showModal("login-modal");
}


function showRegister(userType = "") {
    showModal("register-modal");

    if (!userType) return;

    const roleSelect =
        document.getElementById("register-role");

    if (roleSelect) {
        roleSelect.value = userType;
    }
}


function showForgotPassword() {
    closeModal("login-modal");

    showToast(
        "Password Reset",
        "Password reset functionality will be available soon.",
        "info"
    );
}


/* =========================================================
   DISEASE DETECTION
   ========================================================= */

/*
 * Opens disease detection modal if the
 * homepage uses one.
 */

function showCropDiseaseDetector() {
    const modal =
        document.getElementById(
            "disease-detection-modal"
        );

    if (modal) {
        showModal(
            "disease-detection-modal"
        );
    }
}


function triggerFileUpload() {
    const input =
        document.getElementById(
            "crop-image-input"
        );

    if (input) {
        input.click();
    }
}


async function handleImageUpload(event) {
    const file =
        event.target.files?.[0];

    if (!file) return;


    const uploadArea =
        document.getElementById(
            "upload-area"
        );

    const resultsSection =
        document.getElementById(
            "detection-results"
        );

    const resultContent =
        document.getElementById(
            "result-content"
        );


    if (!uploadArea) return;


    /*
     * Basic file validation
     */

    if (!file.type.startsWith("image/")) {
        showToast(
            "Invalid File",
            "Please upload a valid image.",
            "error"
        );

        event.target.value = "";
        return;
    }


    /*
     * Maximum 5 MB
     */

    const maxSize =
        5 * 1024 * 1024;

    if (file.size > maxSize) {
        showToast(
            "File Too Large",
            "Please upload an image smaller than 5 MB.",
            "error"
        );

        event.target.value = "";
        return;
    }


    uploadArea.innerHTML = `
        <i class="fas fa-spinner fa-spin"></i>
        <h3>Analyzing Image...</h3>
        <p>Our AI is examining your crop.</p>
    `;


    const formData =
        new FormData();

    formData.append(
        "crop_image",
        file
    );


    /*
     * Django CSRF
     */

    const csrfInput =
        document.querySelector(
            "[name=csrfmiddlewaretoken]"
        );

    let csrfToken = "";

    if (csrfInput) {
        csrfToken = csrfInput.value;
    }


    /*
     * Send image to Django
     */

    try {
        const response =
            await fetch(
                "/disease-detector/",
                {
                    method: "POST",
                    headers: {
                        "X-CSRFToken":
                            csrfToken,
                    },
                    body: formData,
                }
            );


        if (!response.ok) {
            throw new Error(
                `Server returned ${response.status}`
            );
        }


        const data =
            await response.json();


        if (data.error) {
            throw new Error(
                data.error
            );
        }


        if (resultContent) {
            resultContent.innerHTML = `
                <div class="detection-result">

                    <div class="result-header">

                        <h4>
                            ${escapeHtml(
                                data.disease || "Unknown"
                            )}
                        </h4>

                        <span class="confidence-badge">
                            ${escapeHtml(
                                String(
                                    data.confidence || "N/A"
                                )
                            )} Confidence
                        </span>

                    </div>

                    <div class="result-details">

                        <div class="detail-item">

                            <strong>Status:</strong>

                            <span>
                                ${escapeHtml(
                                    data.status || "Unknown"
                                )}
                            </span>

                        </div>

                        <div class="detail-item">

                            <strong>
                                Recommended Treatment:
                            </strong>

                            <p>
                                ${escapeHtml(
                                    data.advice ||
                                    "No recommendation available."
                                )}
                            </p>

                        </div>

                    </div>

                </div>
            `;
        }


        if (resultsSection) {
            resultsSection.style.display =
                "block";
        }


        showToast(
            "Analysis Complete",
            "AI crop disease analysis completed.",
            "success"
        );

    } catch (error) {
        console.error(
            "Disease detection error:",
            error
        );

        showToast(
            "Analysis Failed",
            "Could not connect to the AI disease detection server.",
            "error"
        );

    } finally {

        uploadArea.innerHTML = `
            <i class="fas fa-camera"></i>
            <h3>Upload Another Image</h3>
            <p>Select another crop image.</p>
        `;

    }
}


/* =========================================================
   HTML SAFETY
   ========================================================= */

function escapeHtml(value) {
    const div =
        document.createElement("div");

    div.textContent =
        String(value);

    return div.innerHTML;
}


/* =========================================================
   LANGUAGE
   ========================================================= */

function initializeLanguage() {
    updateLanguageContent();
}


function toggleLanguageMenu() {
    const menu =
        document.getElementById(
            "language-menu"
        );

    if (!menu) return;

    const isVisible =
        menu.style.visibility === "visible";

    menu.style.opacity =
        isVisible ? "0" : "1";

    menu.style.visibility =
        isVisible ? "hidden" : "visible";
}


function changeLanguage(
    languageCode,
    languageName
) {
    if (!translations[languageCode]) {
        return;
    }

    currentLanguage =
        languageCode;


    const currentLanguageElement =
        document.getElementById(
            "current-language"
        );

    if (currentLanguageElement) {
        currentLanguageElement.textContent =
            languageName;
    }


    updateLanguageContent();

    toggleLanguageMenu();


    showToast(
        "Language Changed",
        `Language changed to ${languageName}.`,
        "success"
    );
}


function updateLanguageContent() {
    const elements =
        document.querySelectorAll(
            "[data-translate]"
        );


    elements.forEach((element) => {
        const key =
            element.getAttribute(
                "data-translate"
            );

        const translation =
            getTranslation(key);

        if (translation) {
            element.textContent =
                translation;
        }
    });


    const placeholderElements =
        document.querySelectorAll(
            "[data-translate-placeholder]"
        );


    placeholderElements.forEach(
        (element) => {
            const key =
                element.getAttribute(
                    "data-translate-placeholder"
                );

            const translation =
                getTranslation(key);

            if (translation) {
                element.placeholder =
                    translation;
            }
        }
    );
}


function getTranslation(key) {
    if (!key) return null;

    const keys =
        key.split(".");


    let translation =
        translations[currentLanguage];


    for (const keyPart of keys) {
        if (
            translation &&
            Object.prototype.hasOwnProperty.call(
                translation,
                keyPart
            )
        ) {
            translation =
                translation[keyPart];

        } else {

            /*
             * English fallback
             */

            translation =
                translations.en;

            for (
                const fallbackKey of keys
            ) {
                if (
                    translation &&
                    Object.prototype.hasOwnProperty.call(
                        translation,
                        fallbackKey
                    )
                ) {
                    translation =
                        translation[
                            fallbackKey
                        ];

                } else {
                    return null;
                }
            }

            break;
        }
    }


    return typeof translation === "string"
        ? translation
        : null;
}


/* =========================================================
   WEATHER INTELLIGENCE
   ========================================================= */

async function initializeWeather() {
    const statusElement =
        document.getElementById(
            "weather-status"
        );

    /*
     * If weather UI doesn't exist on
     * the current page, do nothing.
     */

    if (!statusElement) {
        return;
    }


    const useDefaultLocation = () => {
        updateWeatherUI(
            28.6139,
            77.2090
        );
    };


    /*
     * Try user's location first.
     */

    if (!navigator.geolocation) {
        useDefaultLocation();
        return;
    }


    navigator.geolocation.getCurrentPosition(
        (position) => {
            updateWeatherUI(
                position.coords.latitude,
                position.coords.longitude
            );
        },

        () => {
            /*
             * Fallback:
             * New Delhi
             */

            useDefaultLocation();
        },

        {
            timeout: 3000,
            maximumAge: 300000,
        }
    );
}


async function updateWeatherUI(
    latitude,
    longitude
) {
    try {
        const response =
            await fetch(
                `/api/weather/?lat=${encodeURIComponent(
                    latitude
                )}&lon=${encodeURIComponent(
                    longitude
                )}`
            );


        if (!response.ok) {
            throw new Error(
                "Weather API request failed"
            );
        }


        const data =
            await response.json();


        if (data.error) {
            throw new Error(
                data.error
            );
        }


        const statusElement =
            document.getElementById(
                "weather-status"
            );

        const weatherData =
            document.getElementById(
                "weather-data"
            );


        if (statusElement) {
            statusElement.style.display =
                "none";
        }


        if (weatherData) {
            weatherData.style.display =
                "grid";
        }


        updateElementText(
            "temp-display",
            `${data.temp ?? "--"}°C`
        );

        updateElementText(
            "city-display",
            data.city ?? "Unknown"
        );

        updateElementText(
            "humidity-display",
            data.humidity ?? "--"
        );

        updateElementText(
            "advice-display",
            data.advice ??
                "No weather advice available."
        );

    } catch (error) {

        console.error(
            "Weather error:",
            error
        );

        const statusElement =
            document.getElementById(
                "weather-status"
            );

        if (statusElement) {
            statusElement.textContent =
                "Weather information unavailable.";
        }
    }
}


function updateElementText(
    elementId,
    value
) {
    const element =
        document.getElementById(
            elementId
        );

    if (element) {
        element.textContent =
            value;
    }
}


/* =========================================================
   TOAST NOTIFICATIONS
   ========================================================= */

function showToast(
    title,
    message,
    type = "info"
) {
    const toastContainer =
        document.getElementById(
            "toast-container"
        );


    if (!toastContainer) {
        console.warn(
            title,
            message
        );

        return;
    }


    const toast =
        document.createElement("div");

    toast.className =
        `toast ${type}`;


    const icons = {
        success:
            "fas fa-check-circle",

        error:
            "fas fa-exclamation-circle",

        warning:
            "fas fa-exclamation-triangle",

        info:
            "fas fa-info-circle",
    };


    const icon =
        icons[type] || icons.info;


    toast.innerHTML = `
        <div class="toast-header">

            <div class="toast-title">

                <i class="${icon}"></i>

                ${escapeHtml(title)}

            </div>

            <button
                type="button"
                class="toast-close"
                aria-label="Close notification"
                onclick="closeToast(this)"
            >
                ×
            </button>

        </div>

        <div class="toast-message">
            ${escapeHtml(message)}
        </div>
    `;


    toastContainer.appendChild(
        toast
    );


    requestAnimationFrame(() => {
        toast.style.transform =
            "translateX(0)";
    });


    setTimeout(() => {
        closeToast(
            toast.querySelector(
                ".toast-close"
            )
        );
    }, 5000);
}


function closeToast(button) {
    if (!button) return;

    const toast =
        button.closest(".toast");

    if (!toast) return;


    toast.style.transform =
        "translateX(100%)";


    setTimeout(() => {
        toast.remove();
    }, 300);
}


/* =========================================================
   KEYBOARD EVENTS
   ========================================================= */

document.addEventListener(
    "keydown",
    (event) => {

        /*
         * Close modal with Escape
         */

        if (event.key === "Escape") {

            const openModals =
                document.querySelectorAll(
                    ".modal.show"
                );

            openModals.forEach(
                (modal) => {
                    modal.classList.remove(
                        "show"
                    );
                }
            );

            document.body.style.overflow =
                "";
        }


        /*
         * Disease/chat pages can handle
         * their own Enter behavior.
         *
         * We intentionally don't keep
         * the old fake video-chat logic.
         */
    }
);


/* =========================================================
   ONLINE / OFFLINE
   ========================================================= */

window.addEventListener(
    "online",
    () => {
        showToast(
            "Connection Restored",
            "You are back online.",
            "success"
        );
    }
);


window.addEventListener(
    "offline",
    () => {
        showToast(
            "Connection Lost",
            "You are currently offline.",
            "warning"
        );
    }
);