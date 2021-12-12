package se.kth.jabeja.config;


public enum AnnealingPolicy {
    ANNEALING_LINEAR("LINEAR"),
    ANNEALING_ACCEPTANCE("ACCEPTANCE"),
    ANNEALING_IMPROVED("IMPROVED");
    String name;
    AnnealingPolicy(String name) {
        this.name = name;
    }
    @Override
    public String toString() {
        return name;
    }
}
