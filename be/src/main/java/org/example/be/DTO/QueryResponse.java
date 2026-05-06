package org.example.be.DTO;

public class QueryResponse {
    private String answer;
    private double confidence;
    private int sourcesUsed;

    // getters + setters
    public String getAnswer() {
        return answer;
    }

    public void setAnswer(String answer) {
        this.answer = answer;
    }

    public double getConfidence() {
        return confidence;
    }

    public void setConfidence(double confidence) {
        this.confidence = confidence;
    }

    public int getSourcesUsed() {
        return sourcesUsed;
    }

    public void setSourcesUsed(int sourcesUsed) {
        this.sourcesUsed = sourcesUsed;
    }
}
