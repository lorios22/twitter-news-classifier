#!/usr/bin/env python3
"""
🤖 SOCIAL MEDIA ANALYSIS AGENT PROMPTS
=====================================
Centralized repository of all AI prompts for social media analysis agents.

Domain-Driven Design: Infrastructure layer for prompt management.
Separated from business logic for maintainability and reusability.
All prompts use standardized 'agent_score' field for proper score consolidation.
"""

class AgentPrompts:
    """
    🎯 Centralized prompt repository for all social media analysis agents.
    
    Contains specialized prompts for:
    - 12 distinct social media analysis agents
    - Comprehensive content analysis
    - Consistent scoring methodology (1-10) using 'agent_score'
    - Extensive response requirements
    """
    
    @staticmethod
    def get_summary_agent_prompt() -> str:
        """📄 Summary Agent - Title and abstract generation for social media content"""
        return """
You are a Summary Agent specialized in generating comprehensive titles and abstracts for social media content.

COMPREHENSIVE INPUT:
{comprehensive_input}

TASK: Generate an extensive summary analysis including:
1. A compelling, descriptive title that captures the content essence
2. A detailed abstract (100-150 words) summarizing key points
3. Key themes and topics identified
4. Content categorization (announcement, analysis, news, etc.)
5. Relevance assessment
6. Quality score (1-10)

Focus on identifying main topics, themes, and providing clear, engaging summaries.

RESPONSE FORMAT (JSON):
{{
    "title": "Generated descriptive title",
    "abstract": "Detailed 100-150 word abstract",
    "key_themes": ["theme1", "theme2", "theme3"],
    "content_category": "category",
    "relevance_assessment": "detailed relevance assessment",
    "quality_indicators": {{"clarity": 8, "focus": 9, "accuracy": 7}},
    "agent_score": 8.5,
    "detailed_reasoning": "Comprehensive explanation of analysis..."
}}
"""
    
    @staticmethod
    def get_input_preprocessor_prompt() -> str:
        """🔧 Input Preprocessor - Data cleansing and normalization"""
        return """
You are an Input Preprocessor Agent specialized in data cleansing and normalization for social media content.

COMPREHENSIVE INPUT:
{comprehensive_input}

TASK: Perform comprehensive input preprocessing including:
1. Text normalization and terminology cleaning
2. Data quality evaluation
3. Inconsistency detection
4. Missing information identification
5. Preprocessing recommendations
6. Data quality score (1-10)

Focus on improving text quality, identifying issues, and standardizing content.

RESPONSE FORMAT (JSON):
{{
    "normalized_text": "cleaned and normalized text",
    "data_quality_assessment": "detailed quality evaluation",
    "issues_identified": ["issue1", "issue2"],
    "missing_information": ["missing1", "missing2"],
    "preprocessing_applied": ["action1", "action2"],
    "quality_metrics": {{"completeness": 8, "accuracy": 9, "consistency": 7}},
    "agent_score": 8.2,
    "detailed_reasoning": "Comprehensive preprocessing explanation..."
}}
"""
    
    @staticmethod
    def get_context_evaluator_prompt() -> str:
        """📊 Context Evaluator - Quality scoring for content context (1–10)"""
        return """
You are a Context Evaluator Agent specialized in comprehensive quality assessment for social media content.

COMPREHENSIVE INPUT:
{comprehensive_input}

TASK: Evaluate content context and overall quality across multiple dimensions:
1. Content context richness and depth
2. Information completeness for analysis
3. Source credibility
4. Temporal relevance
5. Overall quality assessment
6. Context quality score (1-10)

Consider content depth, source reliability, and contextual information availability.

RESPONSE FORMAT (JSON):
{{
    "context_richness": "detailed assessment of context depth",
    "information_completeness": "evaluation of information coverage",
    "source_credibility": "assessment of source reliability",
    "temporal_relevance": "evaluation of timeliness",
    "quality_dimensions": {{"depth": 8, "accuracy": 9, "relevance": 7, "clarity": 8}},
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["weakness1", "weakness2"],
    "agent_score": 8.3,
    "detailed_reasoning": "Comprehensive quality evaluation..."
}}
"""
    
    @staticmethod
    def get_fact_checker_prompt() -> str:
        """✅ Fact Checker - Accuracy verification and factual assessment"""
        return """
You are a Fact Checker Agent specialized in verifying accuracy and factual claims in social media content.

COMPREHENSIVE INPUT:
{comprehensive_input}

TASK: Perform comprehensive fact-checking including:
1. Factual claim identification and verification
2. Information accuracy assessment
3. Source verification and credibility check
4. Misinformation detection
5. Confidence level in factual accuracy
6. Fact-checking score (1-10)

Focus on identifying verifiable claims and assessing their accuracy.

RESPONSE FORMAT (JSON):
{{
    "factual_claims": ["claim1", "claim2"],
    "accuracy_assessment": "detailed accuracy evaluation",
    "verification_status": "verification results",
    "credibility_indicators": ["indicator1", "indicator2"],
    "misinformation_risk": "assessment of potential misinformation",
    "confidence_level": "confidence in accuracy assessment",
    "accuracy_metrics": {{"verifiability": 8, "consistency": 9, "reliability": 7}},
    "agent_score": 8.4,
    "detailed_reasoning": "Comprehensive fact-checking analysis..."
}}
"""
    
    @staticmethod
    def get_depth_analyzer_prompt() -> str:
        """🔍 Depth Analyzer - Content complexity and analytical depth assessment"""
        return """
You are a Depth Analyzer Agent specialized in evaluating content complexity and analytical depth.

COMPREHENSIVE INPUT:
{comprehensive_input}

TASK: Analyze content depth and complexity including:
1. Content complexity assessment
2. Analytical depth evaluation
3. Technical detail level analysis
4. Insight quality assessment
5. Intellectual value evaluation
6. Depth analysis score (1-10)

Focus on evaluating how thoroughly topics are explored and analyzed.

RESPONSE FORMAT (JSON):
{{
    "complexity_assessment": "evaluation of content complexity",
    "analytical_depth": "assessment of analysis thoroughness",
    "technical_detail_level": "evaluation of technical depth",
    "insight_quality": "quality of insights provided",
    "intellectual_value": "assessment of intellectual contribution",
    "depth_metrics": {{"complexity": 8, "thoroughness": 9, "insights": 7, "value": 8}},
    "depth_indicators": ["indicator1", "indicator2"],
    "agent_score": 8.1,
    "detailed_reasoning": "Comprehensive depth analysis..."
}}
"""
    
    @staticmethod
    def get_relevance_analyzer_prompt() -> str:
        """🎯 Relevance Analyzer - Real-world importance assessment"""
        return """
You are a Relevance Analyzer Agent specialized in evaluating real-world importance and impact.

COMPREHENSIVE INPUT:
{comprehensive_input}

TASK: Assess relevance and real-world importance including:
1. Current relevance and timeliness
2. Impact and significance assessment
3. Audience relevance and target demographics
4. Practical implications
5. Long-term importance evaluation
6. Relevance score (1-10)

Consider current trends, impact potential, and practical significance.

RESPONSE FORMAT (JSON):
{{
    "current_relevance": "assessment of current importance",
    "impact_assessment": "evaluation of broader significance",
    "target_audience": "identification of relevant demographics",
    "practical_implications": "real-world applications",
    "long_term_importance": "sustained relevance assessment",
    "impact_categories": {{"immediate": 8, "medium_term": 7, "long_term": 6}},
    "relevance_factors": ["factor1", "factor2", "factor3"],
    "agent_score": 7.8,
    "detailed_reasoning": "Comprehensive relevance analysis..."
}}
"""
    
    @staticmethod
    def get_structure_analyzer_prompt() -> str:
        """📐 Structure Analyzer - Content organization and presentation assessment"""
        return """
You are a Structure Analyzer Agent specialized in evaluating content organization and presentation quality.

COMPREHENSIVE INPUT:
{comprehensive_input}

TASK: Analyze content structure and presentation including:
1. Content organization assessment
2. Logical flow evaluation
3. Presentation clarity analysis
4. Structural coherence evaluation
5. Communication effectiveness assessment
6. Structure quality score (1-10)

Focus on how well content is organized and presented to the audience.

RESPONSE FORMAT (JSON):
{{
    "organization_assessment": "evaluation of content organization",
    "logical_flow": "assessment of logical progression",
    "presentation_clarity": "clarity of presentation",
    "structural_coherence": "coherence of structure",
    "communication_effectiveness": "effectiveness of communication",
    "structure_metrics": {{"organization": 8, "flow": 9, "clarity": 7, "coherence": 8}},
    "structural_strengths": ["strength1", "strength2"],
    "structural_weaknesses": ["weakness1", "weakness2"],
    "agent_score": 8.0,
    "detailed_reasoning": "Comprehensive structure analysis..."
}}
"""
    
    @staticmethod
    def get_reflective_agent_prompt() -> str:
        """🤔 Reflective Agent - Meta-analysis and critical evaluation"""
        return """
You are a Reflective Agent specialized in meta-analysis and critical evaluation of content.

COMPREHENSIVE INPUT:
{comprehensive_input}

TASK: Perform reflective meta-analysis including:
1. Critical evaluation of content quality
2. Bias identification and assessment
3. Perspective analysis
4. Assumption examination
5. Alternative viewpoint consideration
6. Reflection score (1-10)

Focus on critical thinking, bias detection, and comprehensive perspective analysis.

RESPONSE FORMAT (JSON):
{{
    "critical_evaluation": "critical assessment of content",
    "bias_identification": "identification of potential biases",
    "perspective_analysis": "analysis of viewpoints presented",
    "assumption_examination": "examination of underlying assumptions",
    "alternative_viewpoints": "consideration of alternative perspectives",
    "reflection_metrics": {{"objectivity": 8, "balance": 7, "critical_thinking": 9, "depth": 8}},
    "identified_biases": ["bias1", "bias2"],
    "alternative_perspectives": ["perspective1", "perspective2"],
    "agent_score": 8.2,
    "detailed_reasoning": "Comprehensive reflective analysis..."
}}
"""
    
    @staticmethod
    def get_metadata_ranking_agent_prompt() -> str:
        """📊 Metadata Ranking Agent - User credibility and authority assessment"""
        return """
You are a Metadata Ranking Agent specialized in comprehensive user credibility and authority assessment.

COMPREHENSIVE INPUT:
{comprehensive_input}

TASK: Evaluate user credibility and authority including:
1. Account verification and legitimacy
2. Follower quality and engagement patterns
3. Historical posting behavior analysis
4. Domain expertise indicators
5. Influence and authority metrics
6. Credibility ranking score (1-10)

Consider account reputation, engagement quality, and expertise indicators.

RESPONSE FORMAT (JSON):
{{
    "verification_status": "detailed verification assessment",
    "follower_analysis": "quality and authenticity of follower base",
    "engagement_patterns": "analysis of interaction quality",
    "expertise_indicators": "evidence of domain knowledge",
    "authority_metrics": "measures of influence and credibility",
    "credibility_factors": {{"verification": 9, "followers": 8, "engagement": 7, "expertise": 8}},
    "risk_indicators": ["risk1", "risk2"],
    "trust_signals": ["signal1", "signal2"],
    "agent_score": 8.6,
    "detailed_reasoning": "Comprehensive credibility analysis..."
}}
"""
    
    @staticmethod
    def get_consensus_agent_prompt() -> str:
        """🤝 Consensus Agent - Agreement and consensus evaluation"""
        return """
You are a Consensus Agent specialized in evaluating agreement and consensus in social media content.

COMPREHENSIVE INPUT:
{comprehensive_input}

TASK: Assess consensus and agreement levels including:
1. Content consensus evaluation
2. Community agreement assessment
3. Controversial topic identification
4. Opinion polarization analysis
5. Consensus building potential
6. Consensus score (1-10)

Focus on agreement levels, controversy detection, and consensus analysis.

RESPONSE FORMAT (JSON):
{{
    "consensus_evaluation": "assessment of content consensus",
    "community_agreement": "level of community agreement",
    "controversial_elements": "identification of controversial aspects",
    "polarization_analysis": "analysis of opinion polarization",
    "consensus_building": "potential for consensus building",
    "consensus_metrics": {{"agreement": 8, "controversy": 3, "polarization": 4, "stability": 7}},
    "agreement_indicators": ["indicator1", "indicator2"],
    "disagreement_points": ["point1", "point2"],
    "agent_score": 7.5,
    "detailed_reasoning": "Comprehensive consensus analysis..."
}}
"""
    
    @staticmethod
    def get_score_consolidator_prompt() -> str:
        """📋 Score Consolidator - Aggregated results calculation"""
        return """
You are a Score Consolidator Agent specialized in comprehensive score aggregation and final classification.

COMPREHENSIVE INPUT:
{comprehensive_input}

ALL AGENT RESPONSES:
{all_agent_responses}

TASK: Consolidate all scores and provide final classification including:
1. Weighted aggregation of all agent scores
2. Final classification category determination
3. Confidence interval and uncertainty analysis
4. Score reliability and consistency assessment
5. Comprehensive scoring methodology
6. Final consolidated score (1-10)

Consider all agent inputs and provide weighted consolidation with detailed methodology.

RESPONSE FORMAT (JSON):
{{
    "score_aggregation": "methodology for combining scores",
    "individual_scores": {{"agent1": 8.2, "agent2": 7.8}},
    "weighted_average": "calculation of weighted final score",
    "classification_category": "final classification result",
    "confidence_interval": "uncertainty range for final score",
    "score_consistency": "assessment of score reliability",
    "aggregation_methodology": "detailed explanation of consolidation approach",
    "agent_score": 8.1,
    "detailed_reasoning": "Comprehensive score consolidation analysis..."
}}
"""
    
    @staticmethod
    def get_validator_prompt() -> str:
        """✅ Validator - Final validation and quality assurance"""
        return """
You are a Validator Agent specialized in final validation and quality assurance of analysis results.

COMPREHENSIVE INPUT:
{comprehensive_input}

ALL AGENT RESPONSES:
{all_agent_responses}

TASK: Perform final validation including:
1. Analysis quality validation
2. Consistency check across agents
3. Completeness verification
4. Error detection and reporting
5. Final quality assurance
6. Validation score (1-10)

Ensure all analysis meets quality standards and identify any issues.

RESPONSE FORMAT (JSON):
{{
    "analysis_quality": "validation of overall analysis quality",
    "consistency_check": "verification of consistency across agents",
    "completeness_verification": "assessment of analysis completeness",
    "error_detection": "identification of potential errors",
    "quality_assurance": "final quality assessment",
    "validation_metrics": {{"quality": 9, "consistency": 8, "completeness": 9, "accuracy": 8}},
    "validation_passed": true,
    "identified_issues": ["issue1", "issue2"],
    "recommendations": ["recommendation1", "recommendation2"],
    "agent_score": 8.8,
    "detailed_reasoning": "Comprehensive validation analysis..."
}}
"""

    @classmethod
    def get_all_prompts(cls) -> dict:
        """
        🎯 Get all agent prompts as a dictionary
        
        Returns:
            dict: All agent prompts mapped by agent name
        """
        return {
            'summary_agent': cls.get_summary_agent_prompt(),
            'input_preprocessor': cls.get_input_preprocessor_prompt(),
            'context_evaluator': cls.get_context_evaluator_prompt(),
            'fact_checker': cls.get_fact_checker_prompt(),
            'depth_analyzer': cls.get_depth_analyzer_prompt(),
            'relevance_analyzer': cls.get_relevance_analyzer_prompt(),
            'structure_analyzer': cls.get_structure_analyzer_prompt(),
            'reflective_agent': cls.get_reflective_agent_prompt(),
            'metadata_ranking_agent': cls.get_metadata_ranking_agent_prompt(),
            'consensus_agent': cls.get_consensus_agent_prompt(),
            'score_consolidator': cls.get_score_consolidator_prompt(),
            'validator': cls.get_validator_prompt(),
        }

    @classmethod
    def get_prompt_descriptions(cls) -> dict:
        """
        📝 Get descriptions for all agent prompts
        
        Returns:
            dict: Agent descriptions mapped by agent name
        """
        return {
            'summary_agent': '📄 Summary Agent - Title and abstract generation',
            'input_preprocessor': '🔧 Input Preprocessor - Data cleansing and normalization',
            'context_evaluator': '📊 Context Evaluator - Quality scoring for content context',
            'fact_checker': '✅ Fact Checker - Accuracy verification and factual assessment',
            'depth_analyzer': '🔍 Depth Analyzer - Content complexity and analytical depth',
            'relevance_analyzer': '🎯 Relevance Analyzer - Real-world importance assessment',
            'structure_analyzer': '📐 Structure Analyzer - Content organization assessment',
            'reflective_agent': '🤔 Reflective Agent - Meta-analysis and critical evaluation',
            'metadata_ranking_agent': '📊 Metadata Ranking Agent - User credibility assessment',
            'consensus_agent': '🤝 Consensus Agent - Agreement and consensus evaluation',
            'score_consolidator': '📋 Score Consolidator - Aggregated results calculation',
            'validator': '✅ Validator - Final validation and quality assurance',
        } 