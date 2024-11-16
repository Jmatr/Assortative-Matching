# Load necessary libraries
library(ggplot2)
library(reshape2)

# Read the dataset
data <- read.csv("cohort_indices.csv")

# Select relevant columns and rename them for the legend
indices <- data[, c("Cohort", "QOR", "NT", "NT_single", "Normalized_Agg_LR", "Normalized_LRH", "Normalized_LRL")]
colnames(indices) <- c("Cohort", 
                       "Odds ratio (CCM)", 
                       "Trace", 
                       "TraceSingle", 
                       "Agg LR (EMZ)", 
                       "LR_H (EMZ)", 
                       "LR_L (EMZ)")

# Melt the data for plotting
melted_data <- melt(indices, id.vars = "Cohort", 
                    variable.name = "Index", value.name = "Value")

# Define line styles, point shapes, and colors for each index
line_styles <- c("Odds ratio (CCM)" = "dashed",
                 "Trace" = "solid",
                 "TraceSingle" = "dashed",
                 "Agg LR (EMZ)" = "solid",
                 "LR_H (EMZ)" = "dashed",
                 "LR_L (EMZ)" = "dotdash")

point_shapes <- c("Odds ratio (CCM)" = 22,  # Solid square
                  "Trace" = 21,            # Solid circle
                  "TraceSingle" = NA,      # No points
                  "Agg LR (EMZ)" = 21,     # Solid circle
                  "LR_H (EMZ)" = NA,       # No points
                  "LR_L (EMZ)" = NA)       # No points

colors <- c("Odds ratio (CCM)" = "blue",
            "Trace" = "red",
            "TraceSingle" = "red",
            "Agg LR (EMZ)" = "orange",
            "LR_H (EMZ)" = "orange",
            "LR_L (EMZ)" = "orange")

fill_colors <- c("Odds ratio (CCM)" = "blue",
                 "Trace" = "red",
                 "Agg LR (EMZ)" = "orange")  # Fill colors for solid points

# Plot the indices over years
ggplot(melted_data, aes(x = Cohort, y = Value, color = Index, group = Index, linetype = Index, shape = Index)) +
  geom_line(size = 1) +
  geom_point(size = 3, aes(fill = Index), color = "black") +
  scale_linetype_manual(values = line_styles) +
  scale_shape_manual(values = point_shapes) +
  scale_color_manual(values = colors) +
  scale_fill_manual(values = fill_colors) +
  labs(title = "Normalized Assortativity Measures Over Men's Birth Cohorts",
       x = "Men's Birth Cohort",
       y = "Normalized Assortativity Measures",
       color = "Index",
       linetype = "Index",
       shape = "Index",
       # fill = "Index") +
  theme_minimal() +
  theme(legend.position = "bottom")


ggsave("Normalized_Assortativity_Measures.png")

