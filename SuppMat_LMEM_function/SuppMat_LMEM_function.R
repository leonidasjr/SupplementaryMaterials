library(lme4)
library(emmeans)
library(lmerTest)
library(tidyverse)
library(MuMIn)

significant_mixed_models <- function(d_vars, fixed_effect, random_effect, data, alpha = 0.05) {
  results <- list()
  
  for (d_var in d_vars) {
    formula <- as.formula(paste(d_var, "~", fixed_effect, "+ (1|", random_effect, ")"))
    
    if (!random_effect %in% colnames(data)) {
      stop(paste("Random effect", random_effect, "not found in data."))
    }
    
    model <- try(lmer(formula, data = data), silent = TRUE)
    
    if (inherits(model, "try-error")) {
      cat("Error fitting model for", d_var, "\n")
      next
    }
    
    fixed_effects <- summary(model)$coefficients
    
    if (!"Pr(>|t|)" %in% colnames(fixed_effects)) {
      cat("No p-values returned for", d_var, "\n")
      next
    }
    
    p_values <- fixed_effects[, "Pr(>|t|)"]
    
    if (length(p_values) > 1 && any(p_values[-1] <= alpha, na.rm = TRUE)) {
      cat("\n", "===========", d_var, "===========\n")
      print(summary(model))
      
      r2 <- try(MuMIn::r.squaredGLMM(model), silent = TRUE)
      
      if (!inherits(r2, "try-error")) {
        cat("\nEffect size (Nakagawa & Schielzeth, 2013):\n")
        cat("Marginal R² (fixed effects):", round(r2[1], 3), "\n")
        cat("Conditional R² (fixed + random effects):", round(r2[2], 3), "\n")
      }
    }
  }
}

# -------------------------
# 1. Choose file by dialog box
# -------------------------
data_file <- file.choose()

# -------------------------
# 2. Read dataset
# -------------------------
ds_CadLin <- read.delim(data_file, stringsAsFactors = TRUE)

# -------------------------
# 3. Inspect structure
# -------------------------
str(ds_CadLin)

# Optional but recommended
ds_CadLin$DIALECT <- factor(ds_CadLin$DIALECT)
ds_CadLin$SPEAKER <- factor(ds_CadLin$SPEAKER)

# -------------------------
# 4. Define variables
# -------------------------
d_vars <- names(ds_CadLin)[sapply(ds_CadLin, is.numeric)]
fixed_effect <- "DIALECT"
random_effect <- "SPEAKER"

# -------------------------
# 5. Save output in same folder as dataset
# -------------------------
output_file <- file.path(dirname(data_file), "SuppMat_lmem_report.txt")

sink(output_file, split = TRUE)
significant_mixed_models(d_vars, fixed_effect, random_effect, ds_CadLin)
sink()

cat("\nMixed-Effects Modeling ended.")
cat("---------------------------------")
cat("\nOutput saved in:\n", output_file, "\n")