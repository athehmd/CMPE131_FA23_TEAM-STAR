//
//  main.cpp
//  sentiment analyzer
//
//  Created by Ather Ahmed on 8/28/23.
//

#include <iostream>
#include <string>
#include <algorithm>
#include <vector>

std::string toLowerCase(const std::string& str) {
    std::string lowerStr = str;
    std::transform(lowerStr.begin(), lowerStr.end(), lowerStr.begin(), ::tolower);
    return lowerStr;
}

std::string analyzeSentiment(const std::string& text) {
    std::vector<std::string> positiveKeywords = {"good", "happy", "excellent", "awesome", "cool", "great", "Energetic", "Joyful", "Intelligent", "Kind", "Creative", "Brave", "Confident", "Empathetic", "Generous", "Honest", "Optimistic", "Patient", "Reliable", "Strong", "Wise", "Charismatic", "Grateful", "Humble", "Loyal", "Passionate", "Radiant", "Serene", "Thoughtful", "love", "beautiful", "entertaining" };
    std::vector<std::string> negativeKeywords = {"bad", "sad", "terrible", "awful", "ugly", "horrible", "Abrasive" "Annoying", "Arrogant", "Boring", "Brutal", "Clumsy", "Cowardly", "Cruel", "Dishonest", "Disruptive", "Dull", "Egotistical", "Foolish", "Greedy", "Hateful", "Hypocritical", "Ignorant", "Impatient", "Inconsiderate", "Indecisive", "Inflexible", "Intolerant", "Jealous", "Lazy," "Loud", "Miserly", "Obnoxious", "Pessimistic", "Reckless", "Rude", "Selfish", "Stubborn", "Unfriendly", "Unkind", "Unreliable", "Untrustworthy", "Vain", "Vindictive", "Weak-willed", "Whiny" };
    
    std::string lowerText = toLowerCase(text);
    
    int positiveCount = 0;
    int negativeCount = 0;
    
    for (const std::string& keyword : positiveKeywords) {
        if (lowerText.find(toLowerCase(keyword)) != std::string::npos) {
            positiveCount++;
        }
    }
    
    for (const std::string& keyword : negativeKeywords) {
        if (lowerText.find(toLowerCase(keyword)) != std::string::npos) {
            negativeCount++;
        }
    }
    
    if (positiveCount > negativeCount) {
        return "Positive";
    } else if (negativeCount > positiveCount) {
        return "Negative";
    } else {
        return "Neutral";
    }
}

int main() {
    bool rerun = true;
    while(rerun) {
        std::string text, answer;
        std::cout << "Enter a text string: ";
        std::getline(std::cin, text);
        
        std::string sentiment = analyzeSentiment(text);
        std::cout << "Sentiment: " << sentiment << std::endl;
        
        std::cout << "Would you like to try again? (yes or no)" << std::endl;
        std::getline(std::cin, answer);
        
        if(answer == "no") { rerun = false; }
    }
    
    return 0;
}
