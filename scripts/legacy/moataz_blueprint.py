#!/usr/bin/env python3
"""
Moataz AI Platform Engineering Blueprint
Prompt 01 — Product Vision, Master Analysis & Engineering Foundation

Generates a comprehensive 40-section engineering blueprint PDF using ReportLab.
"""

import os
import sys
import hashlib
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm, cm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, CondPageBreak, HRFlowable
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FONT REGISTRATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import platform
_IS_MAC = platform.system() == 'Darwin'
if _IS_MAC:
    FONT_DIR = os.path.expanduser('~/.openclaw/workspace/fonts')
else:
    FONT_DIR = '/usr/share/fonts'

pdfmetrics.registerFont(TTFont('FreeSerif', f'{FONT_DIR}/truetype/freefont/FreeSerif.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-Bold', f'{FONT_DIR}/truetype/freefont/FreeSerifBold.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-Italic', f'{FONT_DIR}/truetype/freefont/FreeSerifItalic.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-BoldItalic', f'{FONT_DIR}/truetype/freefont/FreeSerifBoldItalic.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans', f'{FONT_DIR}/truetype/dejavu/DejaVuSansMono.ttf'))

registerFontFamily('FreeSerif', normal='FreeSerif', bold='FreeSerif-Bold',
                    italic='FreeSerif-Italic', boldItalic='FreeSerif-BoldItalic')
registerFontFamily('DejaVuSans', normal='DejaVuSans', bold='DejaVuSans')

# Install font fallback for mixed-language text
PDF_SKILL_DIR = '/home/z/my-project/skills/pdf'
_scripts = os.path.join(PDF_SKILL_DIR, 'scripts')
if _scripts not in sys.path:
    sys.path.insert(0, _scripts)
from pdf import install_font_fallback
install_font_fallback()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CASCADE PALETTE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAGE_BG       = colors.HexColor('#f4f5f5')
SECTION_BG    = colors.HexColor('#eef0f0')
CARD_BG       = colors.HexColor('#ebeeef')
TABLE_STRIPE  = colors.HexColor('#f2f4f4')
HEADER_FILL   = colors.HexColor('#344e5b')
COVER_BLOCK   = colors.HexColor('#586a74')
BORDER        = colors.HexColor('#beccd4')
ICON          = colors.HexColor('#5187a1')
ACCENT        = colors.HexColor('#297ca6')
ACCENT_2      = colors.HexColor('#bb6c52')
TEXT_PRIMARY   = colors.HexColor('#171819')
TEXT_MUTED     = colors.HexColor('#848a8d')
SEM_SUCCESS   = colors.HexColor('#417251')
SEM_WARNING   = colors.HexColor('#997b3e')
SEM_ERROR     = colors.HexColor('#a04b43')
SEM_INFO      = colors.HexColor('#3f668e')

TABLE_HEADER_COLOR = HEADER_FILL
TABLE_HEADER_TEXT  = colors.white
TABLE_ROW_EVEN     = colors.white
TABLE_ROW_ODD      = TABLE_STRIPE

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE SETUP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAGE_W, PAGE_H = A4
LEFT_MARGIN = 0.85 * inch
RIGHT_MARGIN = 0.85 * inch
TOP_MARGIN = 0.75 * inch
BOTTOM_MARGIN = 0.75 * inch
AVAILABLE_WIDTH = PAGE_W - LEFT_MARGIN - RIGHT_MARGIN

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STYLES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
styles = getSampleStyleSheet()

# TOC styles
toc_level0 = ParagraphStyle(
    name='TOCLevel0', fontName='FreeSerif-Bold', fontSize=12, leading=20,
    leftIndent=20, spaceBefore=6, spaceAfter=3, textColor=TEXT_PRIMARY
)
toc_level1 = ParagraphStyle(
    name='TOCLevel1', fontName='FreeSerif', fontSize=10.5, leading=16,
    leftIndent=44, spaceBefore=2, spaceAfter=2, textColor=TEXT_MUTED
)

# Heading styles
h1_style = ParagraphStyle(
    name='H1Style', fontName='FreeSerif-Bold', fontSize=18, leading=24,
    spaceBefore=18, spaceAfter=10, textColor=HEADER_FILL, alignment=TA_LEFT
)
h2_style = ParagraphStyle(
    name='H2Style', fontName='FreeSerif-Bold', fontSize=13, leading=18,
    spaceBefore=12, spaceAfter=6, textColor=ACCENT, alignment=TA_LEFT
)
h3_style = ParagraphStyle(
    name='H3Style', fontName='FreeSerif-Bold', fontSize=11.5, leading=16,
    spaceBefore=8, spaceAfter=4, textColor=COVER_BLOCK, alignment=TA_LEFT
)

# Body styles
body_style = ParagraphStyle(
    name='BodyStyle', fontName='FreeSerif', fontSize=10.5, leading=17,
    spaceBefore=0, spaceAfter=6, alignment=TA_JUSTIFY,
    textColor=TEXT_PRIMARY
)
body_indent_style = ParagraphStyle(
    name='BodyIndent', fontName='FreeSerif', fontSize=10.5, leading=17,
    spaceBefore=0, spaceAfter=6, alignment=TA_JUSTIFY,
    textColor=TEXT_PRIMARY, leftIndent=20
)
bullet_style = ParagraphStyle(
    name='BulletStyle', fontName='FreeSerif', fontSize=10.5, leading=17,
    spaceBefore=2, spaceAfter=2, alignment=TA_LEFT,
    textColor=TEXT_PRIMARY, leftIndent=28, bulletIndent=14,
    bulletFontName='FreeSerif', bulletFontSize=10.5
)

# Table styles
table_header_style = ParagraphStyle(
    name='TableHeader', fontName='FreeSerif-Bold', fontSize=10,
    textColor=colors.white, alignment=TA_CENTER, leading=14
)
table_cell_style = ParagraphStyle(
    name='TableCell', fontName='FreeSerif', fontSize=9.5,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT, leading=13
)
table_cell_center = ParagraphStyle(
    name='TableCellCenter', fontName='FreeSerif', fontSize=9.5,
    textColor=TEXT_PRIMARY, alignment=TA_CENTER, leading=13
)

# Caption style
caption_style = ParagraphStyle(
    name='CaptionStyle', fontName='FreeSerif-Italic', fontSize=9,
    leading=13, alignment=TA_CENTER, textColor=TEXT_MUTED,
    spaceBefore=3, spaceAfter=6
)

# Callout style
callout_style = ParagraphStyle(
    name='CalloutStyle', fontName='FreeSerif-Italic', fontSize=10.5,
    leading=16, alignment=TA_LEFT, textColor=ACCENT,
    leftIndent=24, rightIndent=12, spaceBefore=8, spaceAfter=8,
    borderColor=ACCENT, borderWidth=0, borderPadding=6
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TOC DOC TEMPLATE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TocDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, 'bookmark_name'):
            level = getattr(flowable, 'bookmark_level', 0)
            text = getattr(flowable, 'bookmark_text', '')
            key = getattr(flowable, 'bookmark_key', '')
            self.notify('TOCEntry', (level, text, self.page, key))

def add_heading(text, style, level=0):
    key = 'h_%s' % hashlib.md5(text.encode()).hexdigest()[:8]
    p = Paragraph('<a name="%s"/>%s' % (key, text), style)
    p.bookmark_name = text
    p.bookmark_level = level
    p.bookmark_text = text
    p.bookmark_key = key
    return p

# Orphan prevention threshold
H1_ORPHAN_THRESHOLD = (PAGE_H - TOP_MARGIN - BOTTOM_MARGIN) * 0.15

def add_major_section(text):
    return [
        CondPageBreak(H1_ORPHAN_THRESHOLD),
        add_heading(text, h1_style, level=0),
    ]

def add_subsection(text):
    return [add_heading(text, h2_style, level=1)]

def add_subsubsection(text):
    return [add_heading(text, h3_style, level=1)]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HELPER FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def make_table(data, col_widths, caption_text=None):
    """Create a styled table with optional caption."""
    t = Table(data, colWidths=col_widths, hAlign='CENTER')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), TABLE_HEADER_TEXT),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [TABLE_ROW_EVEN, TABLE_ROW_ODD]),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements = [Spacer(1, 18), t]
    if caption_text:
        elements.append(Paragraph(caption_text, caption_style))
    elements.append(Spacer(1, 18))
    return elements

def p(text):
    """Shorthand for body paragraph."""
    return Paragraph(text, body_style)

def bp(text):
    """Shorthand for bullet paragraph."""
    return Paragraph(text, bullet_style)

def callout(text):
    """Shorthand for callout/highlight paragraph."""
    return Paragraph(text, callout_style)

def hr():
    """Horizontal rule."""
    return HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=6, spaceBefore=6)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONTENT SECTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def section_01_executive_summary():
    return add_major_section("1. Executive Summary") + [
        p("Moataz AI is a next-generation AI Operating System designed to unify the fragmented landscape of artificial intelligence tools into a single, coherent platform. Unlike existing solutions that address isolated capabilities, such as conversational AI, code generation, or document analysis, Moataz AI integrates nineteen major functional domains into one production-grade system. These domains span AI Chat, AI Workspace, AI Agent Platform, AI Gateway, AI Automation, Project Management, Memory System, Knowledge Base, Code Generation, Sandbox Execution, Document Analysis, Vision AI, Voice AI, Multi-Provider AI, Plugin System, Workflow Engine, Team Collaboration, Android App, and Web Application, with a future Desktop Application planned for subsequent development phases."),
        p("The platform is engineered for global enterprise deployment as a fully managed multi-tenant cloud SaaS service. It adopts a provider-agnostic philosophy, treating OpenAI, Anthropic, Google, Mistral, and locally-hosted models as first-class citizens within a unified orchestration layer. This design decision is not merely technical; it is a strategic hedge against vendor lock-in, a compliance enabler for data sovereignty requirements, and a cost optimization lever that allows enterprises to route AI workloads to the most cost-effective provider without changing application logic."),
        p("From an engineering standpoint, Moataz AI must be built to support thousands of concurrent enterprise tenants, each with their own security boundaries, compliance requirements, and performance expectations. The platform must deliver sub-second AI response times for interactive use cases, maintain 99.95% or higher availability, and scale horizontally to accommodate growth from initial launch through to serving millions of end users. The memory system must provide persistent, contextual continuity across sessions, enabling AI interactions that accumulate understanding over time rather than resetting with each conversation."),
        p("This document serves as the foundational engineering blueprint, the reference artifact that every subsequent development phase, architectural decision, and implementation sprint will rely upon. It does not prescribe technology choices or architectural patterns; those are the subjects of Prompt 02. Instead, it establishes a complete and rigorous understanding of the product itself: what it must be, why it must be that way, and what success looks like before a single line of code is written."),
    ]

def section_02_vision_statement():
    return add_major_section("2. Vision Statement") + [
        p("Moataz AI envisions a world where artificial intelligence is not a collection of disconnected tools but an integrated operating environment, as fundamental and ubiquitous as the operating systems that run our devices today. Just as Windows, macOS, and Linux abstracted hardware complexity and provided a unified application platform, Moataz AI abstracts the complexity of multiple AI providers, models, and modalities into a single operating layer that enterprises and individuals can rely on for every AI-augmented workflow."),
        p("The vision extends beyond mere aggregation. Current market solutions fall into two categories: single-provider platforms that create deep vendor dependency, such as ChatGPT or Claude, and thin orchestration layers that provide basic routing across providers without meaningful integration. Moataz AI occupies the position that neither can: a deeply integrated platform where multi-provider AI is not just routed but orchestrated, where memory persists across interactions, where agents can be composed into complex workflows, and where the workspace paradigm replaces the chat paradigm as the primary interface for AI-assisted work."),
        p("The AI industry is at an inflection point. Enterprise adoption has moved from experimentation to production dependency, yet the tooling ecosystem remains fragmented. Teams use one tool for chat, another for code, a third for document analysis, and a fourth for workflow automation. Each tool has its own context window, its own memory model, and its own security boundary. The cognitive overhead of switching between these tools, and the information loss that occurs at each boundary, represents a productivity tax that grows linearly with the number of tools adopted. Moataz AI eliminates this tax by providing a single platform with a unified context, a unified memory, and a unified security model."),
        p("Ultimately, the vision is for Moataz AI to become the platform on which the next generation of AI-native enterprises are built, the same way that cloud platforms became the foundation for the SaaS generation. This is not a feature product; it is infrastructure."),
    ]

def section_03_mission_statement():
    return add_major_section("3. Mission Statement") + [
        p("Moataz AI's mission is to deliver the world's first fully integrated AI Operating System that empowers enterprises to adopt, orchestrate, and scale artificial intelligence across every workflow without vendor lock-in, context fragmentation, or security compromise. The platform will achieve this through three core commitments that guide every engineering decision and product tradeoff."),
        p("First, Moataz AI commits to provider sovereignty. Every enterprise must retain the freedom to choose, switch, and combine AI providers based on cost, capability, compliance, and latency requirements, without rewriting application logic or migrating data. The platform achieves this through an abstraction layer that normalizes provider differences into a consistent interface while preserving access to provider-specific capabilities when needed. This is not a lowest-common-denominator approach; it is a smart routing and orchestration layer that leverages each provider's strengths."),
        p("Second, Moataz AI commits to contextual continuity. The platform's Memory System and Knowledge Base are not optional features but foundational infrastructure. Every interaction, document, code change, and decision builds upon the accumulated context of previous work. AI assistants within Moataz AI do not suffer from amnesia between sessions; they learn, remember, and reason over an organization's collective knowledge. This commitment has profound implications for the storage architecture, the retrieval systems, and the privacy model, all of which must be designed to support persistent, scoped, and permissioned memory at enterprise scale."),
        p("Third, Moataz AI commits to enterprise-grade security and compliance from day one. The platform will be designed to meet SOC 2 Type II, GDPR, and ISO 27001 requirements at launch, with the architectural foundations in place to support HIPAA, FedRAMP, and other vertical-specific compliance frameworks as the platform expands into regulated industries. Security is not a feature to be added later; it is a structural property of the system's architecture."),
    ]

def section_04_core_philosophy():
    return add_major_section("4. Core Philosophy") + [
        p("The engineering and product philosophy of Moataz AI is rooted in five foundational principles that inform every decision from system architecture to user interface design. These principles are not aspirational statements; they are engineering constraints that must be validated against during every design review and architectural decision record."),
        p("<b>Openness and Provider Agnosticism:</b> The platform treats every AI provider as a pluggable component. No provider receives preferential treatment in the orchestration layer, and no feature should depend on a single provider's proprietary capabilities without a documented fallback strategy. This principle ensures that Moataz AI remains viable regardless of which AI provider dominates the market in any given quarter. The engineering justification is clear: provider dependency creates existential business risk. If a provider changes pricing, introduces breaking changes, or experiences outages, a provider-dependent platform has no recourse. A provider-agnostic platform simply reroutes."),
        p("<b>User Sovereignty Over Data:</b> Users and enterprises own their data unconditionally. The platform must never use customer data for model training, must provide complete data portability, and must support data residency requirements for any jurisdiction. This principle requires that the storage architecture support geographic pinning from the initial design, not as a retrofit. The engineering cost is significant, multi-region data replication, jurisdiction-aware routing, and encryption at rest and in transit, but the market requirement is non-negotiable for enterprise adoption."),
        p("<b>Composability Over Monolith:</b> Every feature within Moataz AI must be composable. The AI Agent Platform must be able to invoke the Code Generation module, which must be able to write to the Knowledge Base, which must be queryable by the Memory System, and all of this must be expressible through the Workflow Engine. Composability is what transforms a collection of features into an operating system. The engineering implication is that every module must expose well-defined interfaces and emit well-defined events, enabling both programmatic composition and visual workflow construction."),
        p("<b>Security as Architecture:</b> Security controls are not layered on top of the system; they are woven into its structure. Authentication, authorization, encryption, audit logging, and tenant isolation are architectural properties, not features. This principle drives decisions such as adopting a zero-trust network model, implementing encryption at the application layer rather than relying solely on transport encryption, and designing the multi-tenancy model with logical isolation from the ground up rather than relying on database-level isolation alone."),
        p("<b>Progressive Complexity:</b> The platform must be simple enough for an individual knowledge worker to adopt in under five minutes, yet powerful enough for an enterprise IT team to configure complex workflows, custom agents, and compliance policies. Every feature must have a default mode that works without configuration and an expert mode that exposes full control. This principle is the bridge between consumer-grade usability and enterprise-grade capability, and it is the single most challenging design constraint in the entire platform."),
    ]

def section_05_primary_objectives():
    return add_major_section("5. Primary Objectives") + [
        p("The primary objectives of Moataz AI are organized into three tiers: launch-critical objectives that must be met before the platform can be considered viable, growth objectives that enable market expansion, and strategic objectives that secure long-term competitive positioning. Each objective is stated with measurable criteria to enable unambiguous validation."),
        p("<b>Launch-Critical Objectives:</b> Deliver a production-ready platform with all core modules operational, including AI Chat with multi-provider support, AI Workspace with persistent sessions, AI Gateway with intelligent routing, Memory System with cross-session recall, Knowledge Base with document ingestion, Code Generation with sandbox execution, and Team Collaboration with role-based access control. Achieve a cold-start onboarding time of under five minutes for individual users and under thirty minutes for enterprise administrators. Deliver initial API response latency below two seconds for the 95th percentile of requests. Attain SOC 2 Type II readiness within six months of launch."),
        p("<b>Growth Objectives:</b> Scale to support 10,000 concurrent enterprise tenants within the first year of operation. Grow the plugin ecosystem to at least 50 community-contributed integrations within the first year. Achieve a monthly active user retention rate above 70% by the end of the first year. Establish presence in at least three geographic regions with local data residency. Onboard at least 20 enterprise customers with annual contract values exceeding $100,000."),
        p("<b>Strategic Objectives:</b> Establish Moataz AI as the de facto standard for multi-provider AI orchestration within three years. Build a self-sustaining plugin marketplace that generates network effects and platform lock-in through ecosystem value rather than proprietary technology. Develop vertical-specific solutions for healthcare, financial services, and legal industries that leverage the platform's compliance architecture. Position the platform for a future where AI agents autonomously manage business processes, making Moataz AI the orchestration layer for the agentic enterprise."),
    ]

def section_06_business_goals():
    return add_major_section("6. Business Goals") + [
        p("The business goals of Moataz AI span revenue generation, market positioning, and competitive moat construction. Each goal is informed by the understanding that the AI platform market is in a rapid consolidation phase where early movers with superior integration capture disproportionate long-term value."),
        p("<b>Revenue Targets:</b> Achieve $1M annual recurring revenue within twelve months of launch through a tiered subscription model that includes a free tier for individual users, a professional tier for small teams, and an enterprise tier with custom pricing. The enterprise tier must account for at least 60% of revenue within the first year, reflecting the platform's enterprise-first positioning. Revenue from the plugin marketplace, taking a platform fee on third-party integrations, should contribute at least 10% of total revenue by the end of year two."),
        p("<b>Market Penetration:</b> Target the global enterprise AI market, which is projected to exceed $300 billion by 2028. The initial go-to-market strategy focuses on technology companies and professional services firms that have already adopted AI tools but are frustrated by fragmentation. These organizations represent the highest-value early adopters because they experience the pain acutely, have the budget to invest, and possess the technical sophistication to evaluate the platform's technical merits. Geographic prioritization follows the cloud maturity curve: North America and Europe first, with MENA and Asia-Pacific expansion in year two."),
        p("<b>Competitive Positioning:</b> Moataz AI does not compete directly with AI providers like OpenAI or Anthropic; it competes with the fragmented toolchain that enterprises currently assemble manually. The competitive moat is integration depth, not any single feature. A competitor that replicates the AI Chat module has not replicated the Memory System, the Workflow Engine, the Agent Platform, or the compliance architecture. Building all of these simultaneously requires the kind of systems-thinking and integration expertise that is difficult to replicate, and the resulting compound value is greater than the sum of its parts. This is the network effect of platform engineering applied to AI."),
    ]

def section_07_technical_goals():
    return add_major_section("7. Technical Goals") + [
        p("Technical goals define the engineering benchmarks that the platform must meet to fulfill its product and business commitments. These goals are not aspirational targets; they are contract-level requirements that every architectural decision must be validated against."),
    ] + make_table(
        [
            [Paragraph('<b>Technical Goal</b>', table_header_style),
             Paragraph('<b>Target</b>', table_header_style),
             Paragraph('<b>Justification</b>', table_header_style)],
            [Paragraph('AI Response Latency (p50)', table_cell_style),
             Paragraph('< 800ms', table_cell_center),
             Paragraph('Interactive use requires near-instant feedback. Above 1s, users perceive lag and reduce engagement.', table_cell_style)],
            [Paragraph('AI Response Latency (p95)', table_cell_style),
             Paragraph('< 2,000ms', table_cell_center),
             Paragraph('The 95th percentile captures provider-side variability. Two seconds is the upper bound for maintaining user attention.', table_cell_style)],
            [Paragraph('Platform Availability', table_cell_style),
             Paragraph('99.95% uptime', table_cell_center),
             Paragraph('Enterprise SLA requirement. Allows ~4.4 hours of downtime per year, necessitating multi-zone deployment.', table_cell_style)],
            [Paragraph('Concurrent Tenants', table_cell_style),
             Paragraph('10,000+', table_cell_center),
             Paragraph('Year-one growth target. Requires horizontal scaling with efficient resource isolation.', table_cell_style)],
            [Paragraph('AI Provider Support', table_cell_style),
             Paragraph('6+ providers', table_cell_center),
             Paragraph('OpenAI, Anthropic, Google, Mistral, Azure OpenAI, and at least one self-hosted model runtime.', table_cell_style)],
            [Paragraph('Plugin Ecosystem', table_cell_style),
             Paragraph('50+ plugins in Y1', table_cell_center),
             Paragraph('Network effects require a critical mass of integrations to attract enterprise buyers.', table_cell_style)],
            [Paragraph('Data Residency', table_cell_style),
             Paragraph('3+ regions', table_cell_center),
             Paragraph('GDPR, data sovereignty, and latency optimization require multi-region deployment.', table_cell_style)],
            [Paragraph('Deployment Frequency', table_cell_style),
             Paragraph('Daily', table_cell_center),
             Paragraph('CI/CD maturity target. Enables rapid iteration without service disruption.', table_cell_style)],
        ],
        [AVAILABLE_WIDTH * 0.28, AVAILABLE_WIDTH * 0.17, AVAILABLE_WIDTH * 0.55],
        "Table 1: Technical Goals and Targets"
    )

def section_08_user_goals():
    return add_major_section("8. User Goals") + [
        p("User goals define what each user segment must be able to accomplish with Moataz AI. These goals are organized by user type and prioritized by impact on adoption and retention."),
        p("<b>Individual Knowledge Workers</b> seek to amplify their productivity through AI without managing multiple subscriptions, learning multiple interfaces, or losing context between sessions. Their primary goal is to have a single AI companion that understands their work, remembers their preferences, and can assist across writing, analysis, coding, and research without requiring them to re-establish context each time. The success metric for this segment is the reduction in time spent on repetitive cognitive tasks by at least 30% within the first month of adoption."),
        p("<b>Development Teams</b> seek to integrate AI into their software development lifecycle, from code generation and review to testing, debugging, and documentation. Their primary goal is to have AI assistance that understands their codebase, their architectural decisions, and their team conventions, and that can operate within their existing development workflows through the Plugin System and API. The success metric is a measurable increase in development velocity, specifically a 25% or greater reduction in time from ticket to deployment."),
        p("<b>Enterprise IT Administrators</b> seek to deploy AI capabilities across their organization while maintaining security boundaries, compliance requirements, and cost controls. Their primary goal is to provide a governed AI environment where employees can use AI productively without exposing sensitive data to unauthorized providers or creating shadow IT risks. The success metric is the ability to deploy Moataz AI across an organization of 1,000+ users with full audit logging, data residency controls, and provider policy enforcement within two weeks."),
        p("<b>Business Executives</b> seek to understand and optimize their organization's AI usage: which teams are using AI effectively, which workflows benefit most from augmentation, and where investment in AI capabilities yields the highest return. Their primary goal is visibility and control over the organization's AI footprint. The success metric is the availability of dashboards showing AI usage patterns, cost allocation by department, and productivity correlations within the first quarter of deployment."),
    ]

def section_09_long_term_vision():
    return add_major_section("9. Long-term Vision") + [
        p("The long-term vision for Moataz AI extends across a five-to-ten-year horizon, encompassing market evolution, technology shifts, and platform growth trajectories that will fundamentally reshape how enterprises interact with artificial intelligence."),
        p("<b>Years 1-2: Foundation and Market Entry.</b> Establish Moataz AI as the leading multi-provider AI orchestration platform for enterprises. The focus is on building the core platform with all nineteen modules operational, achieving SOC 2 Type II and ISO 27001 certification, and onboarding the first cohort of enterprise customers. By the end of year two, the platform should support 50,000 concurrent users across 5,000 enterprise tenants, with a plugin ecosystem exceeding 100 integrations. The Android app should achieve at least 100,000 downloads with a 4.5+ star rating."),
        p("<b>Years 2-4: Agentic Enterprise.</b> The AI industry is moving decisively toward autonomous agents that can plan, execute, and iterate on complex tasks with minimal human supervision. Moataz AI is positioned to be the orchestration layer for this transformation. The Agent Platform, initially supporting human-in-the-loop workflows, will evolve to support fully autonomous agents that manage business processes: customer support escalation, code review and deployment, financial report generation, and compliance monitoring. The Workflow Engine will support declarative agent composition, enabling enterprises to define complex multi-agent processes visually. By the end of year four, agents created on Moataz AI should handle at least 30% of routine enterprise tasks without human intervention."),
        p("<b>Years 4-7: AI Ecosystem and Platform Network Effects.</b> As the plugin marketplace and agent ecosystem mature, Moataz AI transitions from a product to a platform ecosystem. Third-party developers build and monetize specialized agents and integrations, creating a self-reinforcing cycle where more integrations attract more users, and more users attract more developers. The platform introduces an AI agent marketplace where enterprises can discover, evaluate, and deploy pre-built agents for common industry workflows. By the end of year seven, the marketplace should host over 1,000 agents and integrations, with marketplace revenue contributing 25% or more of total platform revenue."),
        p("<b>Years 7-10: Cognitive Infrastructure.</b> The ultimate vision is for Moataz AI to become invisible infrastructure, as foundational to enterprise operations as cloud computing is today. Organizations will not think of themselves as using Moataz AI any more than they think of themselves as using AWS. The platform's intelligence, automation, and contextual understanding will be embedded into every business process, every decision, and every workflow. This is the realization of the AI Operating System vision: a world where AI is not a tool you pick up but an environment you operate within."),
    ]

def section_10_unique_selling_points():
    return add_major_section("10. Unique Selling Points") + [
        p("Moataz AI's unique selling points are the differentiators that cannot be easily replicated by any single competitor because they emerge from the integration of multiple systems rather than from any individual feature."),
        p("<b>Unified AI Operating System vs. Point Solutions:</b> The most fundamental differentiator is architectural. Existing AI tools are point solutions: ChatGPT for conversation, Copilot for code, Notion AI for documents, Zapier for automation. Each tool operates in isolation with its own context window, its own memory model, and its own billing. Moataz AI unifies these capabilities into a single system with a shared context, a shared memory, and a single subscription. The engineering implication is that the platform must maintain a unified context graph that spans all modules, enabling, for example, a code generation session to reference insights from a document analysis, or a workflow to trigger based on patterns detected in chat conversations."),
        p("<b>Provider-Agnostic AI Orchestration:</b> While other platforms lock users into a single provider, Moataz AI treats AI providers as interchangeable compute resources. This is not simple round-robin routing; it is intelligent orchestration that considers model capabilities, latency requirements, cost constraints, data residency policies, and content type to route each request optimally. The system learns from historical routing decisions to improve its orchestration over time. This capability requires building a provider abstraction layer that normalizes differences in API schemas, token counting, streaming behavior, and error handling across providers."),
        p("<b>Persistent, Scoped Memory System:</b> The Memory System is not a conversation history log. It is a structured, queryable knowledge graph that accumulates understanding over time. It scopes memory at multiple levels: personal memory for individual users, team memory for collaborative contexts, and organizational memory for enterprise-wide knowledge. The memory system enables AI interactions that build upon previous work rather than starting from scratch each time. This is a fundamental capability that no current competitor offers at the depth and granularity that Moataz AI requires."),
        p("<b>Composable Agent Platform:</b> The Agent Platform enables users to create AI agents that combine multiple capabilities, such as reading from the Knowledge Base, generating code, executing it in a Sandbox, and writing results to a Document, all within a single agent workflow. These agents can be triggered manually, scheduled, or activated by events, and they can be composed into larger workflows through the Workflow Engine. This composability is what transforms Moataz AI from a tool into an operating system: agents are the applications, and the platform is the runtime."),
        p("<b>Enterprise-First Compliance Architecture:</b> Moataz AI is designed from the ground up for enterprise compliance. Multi-tenant isolation, audit logging, data residency controls, and encryption at rest and in transit are not add-on features but structural properties of the system. This positions the platform for rapid adoption in regulated industries where competitors built for consumer markets must retrofit compliance capabilities."),
    ]

def section_11_competitive_advantages():
    return add_major_section("11. Competitive Advantages") + [
        p("Moataz AI's competitive advantages are structural, meaning they derive from the platform's architecture and market positioning rather than from any individual feature that a competitor could replicate through focused engineering effort."),
        p("<b>Integration Depth as Moat:</b> A competitor that replicates the AI Chat module has not replicated the integration between AI Chat and the Memory System, Knowledge Base, Agent Platform, and Workflow Engine. The value of Moataz AI compounds with each module added because each module deepens the integration surface and creates more cross-module workflows that are impossible in a fragmented toolchain. This is the same dynamic that made Microsoft Office dominant: Word alone was replicable, but Word plus Excel plus PowerPoint plus Outlook, all sharing data and workflow, was a compound advantage that no single-application competitor could match."),
        p("<b>Provider-Agnostic Neutrality:</b> In a market where major AI providers are building walled gardens, Moataz AI occupies the neutral ground. This neutrality is a trust signal for enterprises that are wary of being locked into any single vendor's ecosystem. The provider-agnostic approach also creates a natural on-ramp for enterprises that want to experiment with multiple providers without committing to any single one. Over time, as the AI provider market consolidates, Moataz AI's neutrality becomes more valuable, not less, because it provides a stable abstraction layer above provider-level disruptions."),
        p("<b>Workspace Paradigm vs. Chat Paradigm:</b> Most AI tools use the chat paradigm: a linear conversation thread with a single AI model. Moataz AI uses the workspace paradigm: a persistent, multi-modal environment where users can arrange AI-assisted tasks spatially, maintain multiple simultaneous contexts, and transition seamlessly between modalities such as chat, document editing, code generation, and workflow configuration. The workspace paradigm is more natural for knowledge workers who already use spatial metaphors in tools like Notion, Figma, and VS Code. It is also more powerful because it enables parallel AI interactions rather than sequential ones."),
        p("<b>Open Plugin Architecture:</b> The Plugin System enables third-party developers to extend the platform without requiring core team involvement. This creates a flywheel effect: more plugins attract more users, more users attract more plugin developers, and the platform's capability surface grows faster than any single team could build. The architectural requirement is a stable, well-documented plugin API with clear versioning, sandboxing, and permission controls that enable third-party code to run safely within the platform."),
    ]

def section_12_target_users():
    return add_major_section("12. Target Users") + [
        p("Moataz AI targets five primary user segments, each with distinct needs, adoption patterns, and value metrics. Understanding these segments at a granular level is essential for prioritizing features, designing onboarding flows, and structuring pricing tiers."),
    ] + make_table(
        [
            [Paragraph('<b>User Segment</b>', table_header_style),
             Paragraph('<b>Size Estimate</b>', table_header_style),
             Paragraph('<b>Primary Need</b>', table_header_style),
             Paragraph('<b>Revenue Potential</b>', table_header_style)],
            [Paragraph('Individual Knowledge Workers', table_cell_style),
             Paragraph('50M+ globally', table_cell_center),
             Paragraph('Productivity amplification across all cognitive tasks', table_cell_style),
             Paragraph('Medium (freemium conversion)', table_cell_center)],
            [Paragraph('Development Teams (5-50)', table_cell_style),
             Paragraph('10M+ globally', table_cell_center),
             Paragraph('AI-integrated software development lifecycle', table_cell_style),
             Paragraph('High (team subscriptions)', table_cell_center)],
            [Paragraph('Enterprise IT Departments', table_cell_style),
             Paragraph('500K+ globally', table_cell_center),
             Paragraph('Governed, compliant AI deployment at scale', table_cell_style),
             Paragraph('Very High (enterprise contracts)', table_cell_center)],
            [Paragraph('Business Executives', table_cell_style),
             Paragraph('5M+ globally', table_cell_center),
             Paragraph('Visibility and control over AI usage and ROI', table_cell_style),
             Paragraph('High (influence enterprise deals)', table_cell_center)],
            [Paragraph('Vertical Industries', table_cell_style),
             Paragraph('Growing rapidly', table_cell_center),
             Paragraph('Industry-specific AI workflows and compliance', table_cell_style),
             Paragraph('Very High (premium verticals)', table_cell_center)],
        ],
        [AVAILABLE_WIDTH * 0.20, AVAILABLE_WIDTH * 0.16, AVAILABLE_WIDTH * 0.40, AVAILABLE_WIDTH * 0.24],
        "Table 2: Target User Segments"
    )

def section_13_user_personas():
    return add_major_section("13. User Personas") + [
        p("User personas represent archetypical users whose goals, frustrations, and workflows must be directly addressed by the platform's design. Each persona includes specific scenarios that illustrate how Moataz AI delivers value."),
        p("<b>Persona 1: Sarah, Senior Data Analyst (Age 32)</b>. Sarah works at a mid-size financial services firm. She spends her day analyzing market data, writing reports, and presenting findings to stakeholders. Currently, she uses ChatGPT for brainstorming, a separate tool for data analysis, and PowerPoint for presentations. The context switching costs her roughly two hours per day. With Moataz AI, Sarah works in a single workspace where her AI assistant understands the data she is analyzing, can generate visualization code on demand, and can draft report sections that reference her findings directly. The Memory System remembers her analytical preferences, her company's reporting format, and the terminology specific to her industry."),
        p("<b>Persona 2: Marcus, Engineering Team Lead (Age 38)</b>. Marcus leads a team of eight developers building a SaaS product. He uses GitHub Copilot for code completion, a separate tool for code review, and yet another for documentation. His team loses context between tools and between sessions. With Moataz AI, Marcus's team works within a shared workspace where the AI understands their entire codebase through the Knowledge Base, generates code that follows their team's conventions, executes tests in the Sandbox, and automatically updates documentation. The Team Collaboration features ensure that all team members share a unified AI context."),
        p("<b>Persona 3: Priya, Chief Information Security Officer (Age 45)</b>. Priya is responsible for AI governance at a Fortune 500 company. She needs to ensure that employees are using AI tools safely, that sensitive data is not being exposed to unauthorized providers, and that all AI interactions are auditable. Currently, she has no visibility into which AI tools employees are using or what data they are sharing. With Moataz AI, Priya has a single pane of glass for AI governance: provider policies that restrict which models can process which data types, complete audit logs of every AI interaction, and real-time dashboards showing usage patterns and potential compliance violations."),
        p("<b>Persona 4: Ahmed, Startup Founder (Age 28)</b>. Ahmed runs a three-person startup that builds custom AI workflows for clients. He needs to rapidly prototype and deploy AI agents that combine multiple capabilities. Currently, he stitches together APIs from different providers using custom code, which is fragile and time-consuming. With Moataz AI, Ahmed uses the Agent Platform and Workflow Engine to visually compose AI agents, test them in the Sandbox, and deploy them for clients. The Plugin System allows him to integrate client-specific data sources without building custom connectors."),
        p("<b>Persona 5: Dr. Chen, Research Director (Age 52)</b>. Dr. Chen leads a research lab at a university hospital. She needs AI assistance for literature review, data analysis, and grant writing, but must ensure that patient data never leaves the hospital's approved computing environment. Currently, she cannot use cloud-based AI tools for any work involving patient data. With Moataz AI's provider-agnostic architecture, Dr. Chen configures the platform to route any request involving patient data to locally-hosted models that run within the hospital's security perimeter, while using cloud-based models for general literature review and writing assistance."),
    ]

def section_14_problems():
    return add_major_section("14. Problems This Platform Solves") + [
        p("Moataz AI addresses a set of interconnected problems that collectively represent the most significant friction in enterprise AI adoption today. Each problem is analyzed with its root cause, its impact on organizations, and the specific mechanism by which Moataz AI resolves it."),
        p("<b>Tool Fragmentation:</b> The average enterprise uses 4.7 distinct AI tools, each with its own interface, context window, memory model, and billing. The root cause is that no single tool addresses the full spectrum of AI-augmented work. The impact is measurable: knowledge workers spend an estimated 30% of their AI-assisted work time managing context transitions between tools rather than performing productive work. Moataz AI resolves this by providing a single platform with a unified context and memory system, eliminating context transitions entirely."),
        p("<b>Vendor Lock-In:</b> Enterprises that commit to a single AI provider face three risks: pricing changes that increase costs without recourse, outages that take down all AI-dependent workflows simultaneously, and capability gaps that cannot be filled because the chosen provider lacks specific features. The root cause is that most AI platforms are built on top of a single provider's API, creating deep technical dependencies. Moataz AI resolves this through its provider-agnostic architecture, which treats providers as interchangeable and enables dynamic switching based on cost, capability, and availability criteria."),
        p("<b>Context Loss and Amnesia:</b> Current AI tools treat every session as independent. When a user closes ChatGPT and returns the next day, the AI has no memory of previous work unless the user manually re-establishes context. This amnesia problem is compounded across teams: when multiple team members use AI tools independently, there is no shared context or accumulated knowledge. The root cause is that most AI tools do not maintain persistent memory systems. Moataz AI resolves this through the Memory System and Knowledge Base, which maintain structured, queryable context that persists across sessions and is shared across teams."),
        p("<b>Security and Compliance Gaps:</b> Enterprise IT departments have no way to govern AI usage when employees use consumer-grade tools on personal accounts. Sensitive data may be exposed to AI providers without appropriate safeguards, audit trails may not exist, and data residency requirements may be violated. The root cause is that consumer AI tools were not designed for enterprise governance. Moataz AI resolves this by providing enterprise-grade security controls, audit logging, data residency enforcement, and provider policy management as first-class platform capabilities."),
        p("<b>Workflow Inefficiency:</b> Even when AI tools work well for individual tasks, they do not compose into end-to-end workflows. A user cannot create a workflow that says: read this document, extract key findings, generate a summary, cross-reference with our knowledge base, and draft an email to stakeholders. The root cause is that current tools are designed for isolated interactions, not composable processes. Moataz AI resolves this through the Workflow Engine and Agent Platform, which enable users to compose AI-powered workflows that span multiple modules and execute automatically."),
    ]

def section_15_user_journey():
    return add_major_section("15. Expected User Journey") + [
        p("The user journey from discovery to daily dependence on Moataz AI follows a carefully designed progression that minimizes friction at each stage while building toward deep platform engagement."),
        p("<b>Discovery:</b> Users discover Moataz AI through multiple channels: organic search for AI platform alternatives, referrals from colleagues who use the platform, content marketing that demonstrates the unified workspace concept, and enterprise IT evaluations. The discovery experience must communicate the platform's core value proposition within thirty seconds: one platform for all your AI needs, with memory that persists and providers you can switch."),
        p("<b>Onboarding (0-5 minutes):</b> The onboarding flow must be ruthlessly efficient. New users authenticate, select their preferred AI provider, and are placed into a pre-configured workspace with a guided tutorial that demonstrates the three most impactful features: AI Chat with persistent memory, document analysis, and code generation. The tutorial is not a video; it is an interactive walkthrough where the user performs real tasks. By the end of onboarding, the user has had at least three successful AI interactions and has experienced the memory system firsthand by asking a follow-up question that references a previous answer."),
        p("<b>First Value Moment (5-30 minutes):</b> The first value moment occurs when the user realizes that Moataz AI remembers their context across interactions. This might happen when they return to a workspace after a break and the AI references their previous work, or when they switch from chat to document analysis and the AI already understands what they are working on. This moment must occur within the first thirty minutes or the risk of churn increases dramatically."),
        p("<b>Power User Progression (1-30 days):</b> Over the first month, users progressively discover advanced capabilities: the Workflow Engine for automating repetitive tasks, the Agent Platform for creating custom AI assistants, and the Plugin System for integrating with their existing tools. Each discovery deepens engagement and increases switching costs. The platform should surface these capabilities contextually, suggesting workflow automation when it detects repetitive patterns and recommending plugins when it detects that the user is manually transferring data between Moataz AI and another tool."),
        p("<b>Enterprise Adoption (1-6 months):</b> Enterprise adoption follows a bottom-up path where individual users champion the platform within their organizations, leading to team-wide and eventually organization-wide deployment. The enterprise onboarding process includes SSO integration, compliance configuration, provider policy setup, and team workspace provisioning. The target is to complete enterprise onboarding within two weeks for organizations of up to 1,000 users."),
    ]

def section_16_major_features():
    return add_major_section("16. Major Platform Features") + [
        p("The following table catalogs all major platform features, their purpose, and their expected behavior. This feature catalog serves as the authoritative reference for scope definition and prioritization throughout the development lifecycle."),
    ] + make_table(
        [
            [Paragraph('<b>Feature</b>', table_header_style),
             Paragraph('<b>Purpose</b>', table_header_style),
             Paragraph('<b>Expected Behavior</b>', table_header_style)],
            [Paragraph('AI Chat', table_cell_style),
             Paragraph('Conversational AI interface', table_cell_style),
             Paragraph('Multi-turn conversations with persistent memory, provider switching, and context carry-forward', table_cell_style)],
            [Paragraph('AI Workspace', table_cell_style),
             Paragraph('Persistent work environment', table_cell_style),
             Paragraph('Multi-modal workspace with spatial layout, simultaneous contexts, and session persistence', table_cell_style)],
            [Paragraph('AI Agent Platform', table_cell_style),
             Paragraph('Custom AI agent creation', table_cell_style),
             Paragraph('Visual agent builder with capability composition, trigger configuration, and deployment', table_cell_style)],
            [Paragraph('AI Gateway', table_cell_style),
             Paragraph('Multi-provider routing', table_cell_style),
             Paragraph('Intelligent request routing based on capability, cost, latency, and data residency policies', table_cell_style)],
            [Paragraph('AI Automation', table_cell_style),
             Paragraph('Task automation', table_cell_style),
             Paragraph('Event-driven automation with conditional logic, scheduling, and integration triggers', table_cell_style)],
            [Paragraph('Project Management', table_cell_style),
             Paragraph('AI-augmented PM', table_cell_style),
             Paragraph('Task tracking with AI-suggested priorities, timeline estimation, and resource allocation', table_cell_style)],
            [Paragraph('Memory System', table_cell_style),
             Paragraph('Persistent context', table_cell_style),
             Paragraph('Multi-scope memory (personal, team, org) with structured knowledge graph and retrieval', table_cell_style)],
            [Paragraph('Knowledge Base', table_cell_style),
             Paragraph('Document intelligence', table_cell_style),
             Paragraph('Document ingestion, indexing, semantic search, and AI-powered Q&A over organizational knowledge', table_cell_style)],
            [Paragraph('Code Generation', table_cell_style),
             Paragraph('AI-assisted coding', table_cell_style),
             Paragraph('Context-aware code generation with multi-language support and team convention awareness', table_cell_style)],
            [Paragraph('Sandbox Execution', table_cell_style),
             Paragraph('Safe code execution', table_cell_style),
             Paragraph('Isolated execution environment with resource limits, output capture, and security controls', table_cell_style)],
            [Paragraph('Document Analysis', table_cell_style),
             Paragraph('Document understanding', table_cell_style),
             Paragraph('Multi-format document parsing, extraction, summarization, and comparison', table_cell_style)],
            [Paragraph('Vision AI', table_cell_style),
             Paragraph('Image understanding', table_cell_style),
             Paragraph('Image analysis, OCR, visual Q&A, and image generation capabilities', table_cell_style)],
            [Paragraph('Voice AI', table_cell_style),
             Paragraph('Speech interface', table_cell_style),
             Paragraph('Speech-to-text, text-to-speech, and voice-activated AI interactions', table_cell_style)],
            [Paragraph('Multi-Provider AI', table_cell_style),
             Paragraph('Provider abstraction', table_cell_style),
             Paragraph('Unified interface across 6+ AI providers with capability normalization and fallback', table_cell_style)],
            [Paragraph('Plugin System', table_cell_style),
             Paragraph('Extensibility', table_cell_style),
             Paragraph('Third-party plugin API with sandboxing, permissions, and marketplace distribution', table_cell_style)],
            [Paragraph('Workflow Engine', table_cell_style),
             Paragraph('Process orchestration', table_cell_style),
             Paragraph('Visual workflow builder with conditional logic, branching, and error handling', table_cell_style)],
            [Paragraph('Team Collaboration', table_cell_style),
             Paragraph('Shared AI context', table_cell_style),
             Paragraph('Shared workspaces, team memory, role-based access, and collaborative AI sessions', table_cell_style)],
            [Paragraph('Android App', table_cell_style),
             Paragraph('Mobile access', table_cell_style),
             Paragraph('Native Android client with voice AI, push notifications, and offline capabilities', table_cell_style)],
            [Paragraph('Web Application', table_cell_style),
             Paragraph('Primary interface', table_cell_style),
             Paragraph('Responsive web app with full platform capabilities and progressive enhancement', table_cell_style)],
        ],
        [AVAILABLE_WIDTH * 0.18, AVAILABLE_WIDTH * 0.22, AVAILABLE_WIDTH * 0.60],
        "Table 3: Major Platform Features Catalog"
    )

def section_17_core_modules():
    return add_major_section("17. Core Modules") + [
        p("Core modules are those required for the minimum viable platform launch. Each core module is defined with its purpose, key capabilities, and dependencies on other modules."),
        p("<b>AI Chat Module:</b> The conversational AI interface serves as the primary interaction paradigm for users who prefer a dialogue-based workflow. Key capabilities include multi-turn conversation with persistent history, automatic context window management that summarizes earlier conversation turns to maximize the utility of the available token budget, provider switching mid-conversation without losing context, and integration with the Memory System to persist and retrieve conversation insights across sessions. This module depends on the AI Gateway for provider routing and the Memory System for persistent context."),
        p("<b>AI Gateway Module:</b> The gateway is the central orchestration layer that routes AI requests to appropriate providers based on capability requirements, cost constraints, latency targets, data residency policies, and current provider availability. Key capabilities include real-time provider health monitoring with automatic failover, request-level routing policies that can be configured per tenant, token counting normalization across providers with different tokenization schemes, streaming response aggregation, and comprehensive usage metering for billing and analytics. This module has no upstream dependencies; it is the foundation upon which all AI-interacting modules depend."),
        p("<b>Memory System Module:</b> The memory system provides persistent, structured context that accumulates across sessions and scopes. Key capabilities include multi-scope memory with personal, team, and organizational boundaries, automatic memory extraction from AI interactions that identifies and stores key facts, decisions, and preferences without requiring explicit user action, semantic retrieval that surfaces relevant memories based on the current context rather than keyword matching, memory governance that enables administrators to define retention policies, access controls, and deletion rules. This module depends on the AI Gateway for embedding generation and vector operations."),
        p("<b>Knowledge Base Module:</b> The knowledge base ingests, indexes, and enables semantic search over organizational documents and data. Key capabilities include multi-format document ingestion supporting PDF, DOCX, HTML, Markdown, and common data formats, automatic chunking and embedding with configurable strategies, hybrid search combining semantic similarity with keyword matching for optimal recall, citation and provenance tracking that enables users to trace AI responses back to source documents, and incremental ingestion that updates the index as documents change. This module depends on the AI Gateway for embedding generation and the Memory System for cross-referencing."),
        p("<b>AI Workspace Module:</b> The workspace provides a persistent, spatial environment for AI-assisted work. Key capabilities include multi-panel layouts that support simultaneous chat, document editing, code generation, and data visualization, session persistence that preserves the entire workspace state including open panels, scroll positions, and AI context, workspace templates for common workflows such as research, coding, and analysis, and cross-panel context sharing that allows AI in one panel to reference content in another. This module depends on the AI Chat module, Knowledge Base, and Memory System."),
        p("<b>Team Collaboration Module:</b> The collaboration module enables shared AI contexts within teams. Key capabilities include shared workspaces with concurrent editing, team-level memory that accumulates collective knowledge, role-based access control that governs who can create, edit, and delete shared resources, and presence indicators that show when team members are actively working in a shared workspace. This module depends on the Workspace, Memory System, and the platform's authentication and authorization infrastructure."),
    ]

def section_18_future_modules():
    return add_major_section("18. Future Modules") + [
        p("Future modules are planned for post-launch phases. Each is described with its rationale, estimated timeline, and prerequisite core modules."),
        p("<b>Desktop Application (Phase 2, 6-12 months post-launch):</b> A native desktop application for Windows, macOS, and Linux that provides deeper OS integration than the web application. Key capabilities include system-wide keyboard shortcuts for AI access, native file system integration for direct document ingestion, local model execution for air-gapped environments, and offline mode with synchronization. Prerequisites: stable Web Application API, robust synchronization layer, and local model runtime support in the AI Gateway."),
        p("<b>Advanced Agent Marketplace (Phase 2, 6-12 months post-launch):</b> A marketplace where third-party developers can publish and monetize AI agents. Key capabilities include agent discovery with quality ratings and reviews, automated security scanning of submitted agents, usage-based revenue sharing, and enterprise licensing for private agent deployment. Prerequisites: mature Agent Platform with stable APIs, Plugin System with sandboxing, and payment processing infrastructure."),
        p("<b>Vertical Industry Packs (Phase 3, 12-18 months post-launch):</b> Pre-built packages of agents, workflows, knowledge base templates, and compliance configurations for specific industries such as healthcare, legal, financial services, and education. Each pack includes industry-specific terminology databases, regulatory compliance templates, and pre-configured agent workflows. Prerequisites: general platform stability, compliance architecture certification, and domain expert partnerships for content development."),
        p("<b>Real-Time Collaboration Engine (Phase 3, 12-18 months post-launch):</b> Enhanced real-time collaboration features including live cursor tracking, simultaneous AI interaction where multiple users can interact with the same AI instance, collaborative workflow building, and real-time conflict resolution for concurrent edits. Prerequisites: robust WebSocket infrastructure, operational transformation or CRDT-based synchronization, and enhanced presence system."),
        p("<b>AI Model Fine-Tuning Interface (Phase 4, 18-24 months post-launch):</b> A visual interface for fine-tuning AI models on organizational data without requiring machine learning expertise. Key capabilities include dataset preparation tools, fine-tuning job management with cost estimation, A/B testing of fine-tuned vs. base models, and automatic deployment through the AI Gateway. Prerequisites: mature Knowledge Base for training data sourcing, GPU compute infrastructure, and fine-tuning API integrations with AI providers."),
    ]

def section_19_functional_requirements():
    return add_major_section("19. Functional Requirements") + [
        p("Functional requirements define what the system must do. They are organized by module area and classified by priority: P0 (launch-blocking), P1 (launch-desirable), and P2 (post-launch)."),
        p("<b>AI Gateway Requirements:</b> The system must route AI requests to at least six providers with distinct model families (P0). It must normalize request and response schemas across providers into a unified interface (P0). It must support streaming responses with real-time token delivery to the client (P0). It must implement provider health monitoring with automatic failover within five seconds of detecting a provider outage (P0). It must enforce tenant-level provider policies that restrict which providers can process which data types (P0). It must support custom model endpoints for self-hosted models (P1). It must provide request-level cost estimation before execution (P1). It must support prompt template management with version control (P2)."),
        p("<b>Memory System Requirements:</b> The system must persist conversation context across sessions (P0). It must support three memory scopes: personal, team, and organizational (P0). It must perform semantic retrieval of relevant memories based on the current interaction context (P0). It must automatically extract key facts, decisions, and preferences from conversations without explicit user action (P0). It must support memory governance including retention policies, access controls, and deletion (P0). It must provide memory search with both semantic and keyword matching (P1). It must support memory export for data portability (P1). It must enable users to manually annotate and organize memories (P2)."),
        p("<b>Knowledge Base Requirements:</b> The system must ingest documents in PDF, DOCX, HTML, and Markdown formats (P0). It must perform automatic chunking and embedding with configurable strategies (P0). It must support hybrid search combining semantic similarity and keyword matching (P0). It must track citation and provenance for all AI responses that reference knowledge base content (P0). It must support incremental ingestion and automatic re-indexing when documents change (P0). It must handle documents of at least 500 pages without degradation (P1). It must support real-time collaboration on shared knowledge bases (P2)."),
        p("<b>Workflow Engine Requirements:</b> The system must support visual workflow construction with drag-and-drop interface (P0). It must support conditional branching, looping, and error handling in workflows (P0). It must support manual approval steps within automated workflows (P0). It must support event-driven triggers including scheduled, webhook, and internal platform events (P0). It must support workflow versioning with rollback capability (P1). It must support sub-workflow composition for workflow modularity (P1). It must provide workflow analytics including execution time, success rates, and bottleneck identification (P2)."),
    ]

def section_20_nonfunctional_requirements():
    return add_major_section("20. Non-Functional Requirements") + [
        p("Non-functional requirements define the quality attributes that the system must exhibit. These are cross-cutting concerns that apply across all modules and are validated through system-level testing rather than feature-level testing. Each requirement is stated with a measurable criterion and a rationale that explains why the specific threshold was chosen."),
        p("<b>Performance:</b> The system must deliver AI response times below 800ms at the 50th percentile and below 2,000ms at the 95th percentile for standard requests. These thresholds are derived from user experience research showing that perceived responsiveness degrades significantly above one second for interactive tasks. The system must support at least 10,000 concurrent users with no degradation in response times. The system must complete knowledge base search queries in under 500ms for collections of up to one million documents."),
        p("<b>Security:</b> The system must encrypt all data at rest using AES-256 and all data in transit using TLS 1.3. The system must implement multi-tenant isolation that prevents any possibility of cross-tenant data access, even in the event of a software vulnerability. The system must maintain complete audit logs of all AI interactions, data access events, and administrative actions for a minimum of seven years. The system must support multi-factor authentication and integrate with enterprise SSO providers via SAML 2.0 and OpenID Connect."),
        p("<b>Reliability:</b> The system must achieve 99.95% availability, measured on a rolling monthly basis. The system must implement automatic failover with a maximum recovery time objective of five minutes for any single component failure. The system must maintain data durability of 99.9999999% (nine nines) for all persisted data. The system must implement graceful degradation where, in the event of an AI provider outage, the system automatically routes to alternative providers without user-visible errors."),
        p("<b>Scalability:</b> The system must scale horizontally to support growth from 1,000 to 100,000 concurrent users without requiring architectural changes. The system must support multi-region deployment with data residency enforcement. The system must implement auto-scaling that responds to load changes within three minutes. The system must maintain consistent performance under load through request queuing, rate limiting, and load shedding strategies."),
    ]

def section_21_security_requirements():
    return add_major_section("21. Security Requirements") + [
        p("Security requirements are the most critical non-functional requirements for an enterprise AI platform because the platform processes and stores the most sensitive category of organizational data: the unstructured knowledge and decision-making context of its users. A breach of this data exposes not just documents but the cognitive patterns, strategic thinking, and confidential deliberations of the organization."),
        p("<b>Authentication and Authorization:</b> The platform must support enterprise-grade authentication via SAML 2.0 and OpenID Connect for single sign-on integration. Multi-factor authentication must be available for all user accounts and mandatory for administrator accounts. Authorization must follow the principle of least privilege, with role-based access control at the workspace, team, and organizational levels. API authentication must use short-lived tokens with refresh token rotation and must support IP-based access restrictions for enterprise tenants."),
        p("<b>Data Protection:</b> All data at rest must be encrypted using AES-256 with customer-managed key options for enterprise tenants. All data in transit must be encrypted using TLS 1.3 with certificate pinning for API communications. Tenant data isolation must be enforced at the application layer, not just the database layer, to prevent cross-tenant data leakage even in the event of a SQL injection or similar vulnerability. Data residency must be enforced per tenant, with data never leaving the designated geographic region without explicit tenant configuration."),
        p("<b>AI-Specific Security:</b> The platform must implement prompt injection detection and mitigation for all user-facing AI interactions. The AI Gateway must sanitize AI outputs before rendering to prevent cross-site scripting and content injection attacks. The Sandbox Execution environment must use container-level isolation with resource limits to prevent escape attacks. Provider policy enforcement must prevent sensitive data from being sent to AI providers that do not meet the tenant's security requirements. All AI provider API keys must be stored in a secrets management system with automatic rotation."),
        p("<b>Compliance Frameworks:</b> The platform must be designed to meet SOC 2 Type II requirements at launch. The architecture must support GDPR compliance including data subject access requests, right to erasure, and data portability. The architecture must be compatible with ISO 27001 certification. The design must include the foundations for HIPAA, FedRAMP, and other vertical-specific compliance frameworks, even if full certification is pursued post-launch. Every compliance requirement must have a corresponding architectural control that can be verified through audit."),
    ]

def section_22_performance_requirements():
    return add_major_section("22. Performance Requirements") + [
        p("Performance requirements define the quantitative targets that the platform must meet under specified load conditions. These targets are derived from user experience research, enterprise expectations, and competitive benchmarking."),
    ] + make_table(
        [
            [Paragraph('<b>Metric</b>', table_header_style),
             Paragraph('<b>Target</b>', table_header_style),
             Paragraph('<b>Conditions</b>', table_header_style),
             Paragraph('<b>Measurement Method</b>', table_header_style)],
            [Paragraph('AI Chat First Token', table_cell_style),
             Paragraph('< 500ms', table_cell_center),
             Paragraph('Streaming mode, standard model', table_cell_style),
             Paragraph('Time from request to first streamed token', table_cell_style)],
            [Paragraph('AI Chat Full Response (p50)', table_cell_style),
             Paragraph('< 800ms', table_cell_center),
             Paragraph('Non-streaming, < 500 tokens', table_cell_style),
             Paragraph('End-to-end from request to complete response', table_cell_style)],
            [Paragraph('AI Chat Full Response (p95)', table_cell_style),
             Paragraph('< 2,000ms', table_cell_center),
             Paragraph('Non-streaming, < 500 tokens', table_cell_style),
             Paragraph('Includes provider-side variability', table_cell_style)],
            [Paragraph('Knowledge Base Search', table_cell_style),
             Paragraph('< 500ms', table_cell_center),
             Paragraph('Up to 1M documents', table_cell_style),
             Paragraph('Hybrid semantic + keyword query', table_cell_style)],
            [Paragraph('Memory Retrieval', table_cell_style),
             Paragraph('< 200ms', table_cell_center),
             Paragraph('Per query, up to 10K memories', table_cell_style),
             Paragraph('Semantic retrieval with ranking', table_cell_style)],
            [Paragraph('Document Ingestion', table_cell_style),
             Paragraph('< 30s per 100 pages', table_cell_center),
             Paragraph('PDF with OCR', table_cell_style),
             Paragraph('From upload to searchable index', table_cell_style)],
            [Paragraph('Sandbox Code Execution', table_cell_style),
             Paragraph('< 5s cold start', table_cell_center),
             Paragraph('Standard container', table_cell_style),
             Paragraph('Time from request to execution start', table_cell_style)],
            [Paragraph('Page Load Time (Web)', table_cell_style),
             Paragraph('< 2s', table_cell_center),
             Paragraph('Initial load, 3G connection', table_cell_style),
             Paragraph('Lighthouse performance score > 85', table_cell_style)],
        ],
        [AVAILABLE_WIDTH * 0.22, AVAILABLE_WIDTH * 0.14, AVAILABLE_WIDTH * 0.30, AVAILABLE_WIDTH * 0.34],
        "Table 4: Performance Requirements and Targets"
    )

def section_23_availability_requirements():
    return add_major_section("23. Availability Requirements") + [
        p("Availability requirements define the platform's commitment to uptime and the strategies for maintaining service continuity under adverse conditions. For a global enterprise SaaS platform, availability is not merely a technical metric; it is a business commitment that directly impacts customer trust and contractual obligations."),
        p("<b>SLA Targets:</b> The platform commits to 99.95% availability, measured on a rolling monthly basis. This translates to a maximum of approximately 4.4 hours of unplanned downtime per year. For enterprise customers with premium SLAs, the target is 99.99% availability, or approximately 52 minutes of unplanned downtime per year. These targets exclude scheduled maintenance windows, which must be limited to four hours per month and must occur during the lowest-traffic period for the affected region."),
        p("<b>Disaster Recovery:</b> The platform must maintain a recovery point objective of less than one minute, meaning that no more than one minute of data can be lost in a catastrophic failure. The recovery time objective for a full regional outage must be less than thirty minutes. These objectives require synchronous replication of critical data across availability zones and asynchronous replication across geographic regions. The disaster recovery plan must be tested quarterly through simulated failover exercises."),
        p("<b>Failover Strategy:</b> The platform must implement active-active deployment across at least two availability zones within each region. In the event of a zone failure, traffic must automatically reroute to the remaining zones with no manual intervention. For AI provider failover, the AI Gateway must detect provider outages within five seconds and automatically reroute requests to alternative providers. The failover strategy must be tested through chaos engineering practices, including regular injection of simulated provider outages and zone failures."),
        p("<b>Maintenance Windows:</b> The platform must support zero-downtime deployments through blue-green deployment strategies. All software updates must be deployed without service interruption. Database schema migrations must be backward-compatible and must support rolling deployment. Feature flags must control the activation of new features, enabling gradual rollout and instant rollback if issues are detected."),
    ]

def section_24_scalability_requirements():
    return add_major_section("24. Scalability Requirements") + [
        p("Scalability requirements define how the platform must grow to accommodate increasing load without architectural changes or performance degradation. The scalability model must account for both the predictable growth of existing tenants and the burst capacity requirements of onboarding large enterprise customers."),
        p("<b>Horizontal Scaling:</b> All stateless services must be horizontally scalable through the addition of compute instances. The platform must support automatic scaling based on CPU utilization, memory consumption, request latency, and queue depth. Auto-scaling must respond to load changes within three minutes. The maximum supported scale must be at least 100,000 concurrent users without architectural modifications. Each tenant must be isolated at the application level to prevent resource contention between tenants, often called the noisy neighbor problem."),
        p("<b>Multi-Tenancy Model:</b> The platform must implement a shared-everything multi-tenancy model with logical isolation. Shared infrastructure reduces cost and operational complexity, while logical isolation ensures that no tenant can access another tenant's data or affect another tenant's performance. The tenancy model must support tenant-level resource quotas that prevent any single tenant from consuming disproportionate resources. For enterprise customers with premium requirements, the platform must support dedicated compute instances while sharing the control plane and data plane."),
        p("<b>Data Scalability:</b> The knowledge base must scale to support at least 10 million documents per tenant without search performance degradation. The memory system must scale to support at least 1 million memory entries per user. Document storage must support at least 10 terabytes per tenant. All data stores must support sharding or partitioning strategies that enable horizontal scaling without application-level changes."),
        p("<b>Geographic Scalability:</b> The platform must support deployment in at least three geographic regions at launch with the architectural capacity to expand to any major cloud region. Data residency must be enforced per tenant, with data never leaving the designated region without explicit configuration. Cross-region latency for read operations must be below 100ms. Cross-region replication for write operations must be asynchronous with a maximum lag of five seconds."),
    ]

def section_25_maintainability_requirements():
    return add_major_section("25. Maintainability Requirements") + [
        p("Maintainability requirements define how efficiently the engineering team can modify, extend, and operate the platform over its lifecycle. For a platform expected to serve enterprises for a decade or more, maintainability is a first-class architectural concern that directly impacts velocity, cost, and reliability."),
        p("<b>Code Quality Standards:</b> All production code must maintain a minimum of 80% test coverage for business logic. Critical paths, including authentication, authorization, data isolation, and AI request routing, must maintain 95% or higher coverage. All public APIs must have contract tests that validate request and response schemas. Code review must be mandatory for all changes to production code, with at least one senior engineer approval required. Static analysis must be integrated into the CI pipeline and must pass before any merge."),
        p("<b>Documentation Standards:</b> Every module must have architectural decision records that document the context, decision, and consequences of significant technical choices. All public APIs must have OpenAPI specifications with examples. All configuration parameters must be documented with their purpose, valid ranges, default values, and interdependencies. Runbooks must exist for all operational procedures, including deployment, scaling, failover, and incident response. Documentation must be version-controlled alongside code."),
        p("<b>Observability:</b> The platform must implement three pillars of observability: structured logging, distributed tracing, and metrics. All services must emit structured logs with correlation IDs that enable end-to-end request tracing across service boundaries. Distributed tracing must capture all inter-service calls with latency measurements. Metrics must cover the four golden signals: latency, traffic, errors, and saturation. Alerting must be configured for all SLO violations with escalation paths defined."),
        p("<b>Deployment Practices:</b> The platform must support daily deployments to production without service interruption. All deployments must be automated through a CI/CD pipeline. Feature flags must control the activation of new features, enabling gradual rollout to specific tenant cohorts. Rollback must be achievable within five minutes of detecting a deployment issue. Database migrations must be forward-compatible and must support zero-downtime execution."),
    ]

def section_26_reliability_requirements():
    return add_major_section("26. Reliability Requirements") + [
        p("Reliability requirements define the platform's ability to operate correctly and consistently under both normal and adverse conditions. For an AI operating system that enterprises depend on for mission-critical workflows, reliability is not a desirable attribute but a contractual obligation."),
        p("<b>Fault Tolerance:</b> The platform must tolerate the failure of any single component, including compute instances, database nodes, message queues, and AI provider endpoints, without user-visible impact. The system must implement circuit breakers for all external service calls, including AI provider APIs, with configurable thresholds for opening, half-opening, and closing circuits. The system must implement retry logic with exponential backoff and jitter for transient failures. All critical data must be replicated across at least three availability zones with synchronous replication for write operations."),
        p("<b>Error Recovery:</b> The system must implement automatic recovery for all known failure modes. Recovery procedures must be documented and tested quarterly. For AI provider failures, the system must automatically failover to alternative providers within five seconds. For infrastructure failures, the system must automatically replace failed instances within three minutes. For data corruption events, the system must restore from the most recent backup with a recovery point objective of less than one minute. All error recovery procedures must be idempotent to support safe retry without side effects."),
        p("<b>Data Integrity:</b> The system must guarantee exactly-once processing for all critical operations, including AI request execution, document ingestion, and memory updates. The system must implement optimistic concurrency control for all collaborative editing operations. The system must maintain referential integrity across all related data entities, including workspaces, documents, memories, and workflows. The system must implement checksum validation for all data transfers and storage operations. Data backup integrity must be verified through automated restoration testing on a monthly basis."),
        p("<b>Mean Time Between Failures:</b> The target MTBF for the platform as a whole must exceed 720 hours (approximately one month). The target MTBF for individual AI provider integrations must exceed 168 hours (one week), acknowledging that provider outages are outside the platform's direct control. The target MTTR for any production incident must be below 30 minutes. These targets must be measured and reported monthly, with root cause analysis conducted for any incident that exceeds the MTTR target."),
    ]

def section_27_extensibility_requirements():
    return add_major_section("27. Extensibility Requirements") + [
        p("Extensibility requirements define how the platform can be extended by both the core engineering team and third-party developers. For a platform that aims to become an ecosystem, extensibility is the primary driver of network effects and long-term competitive advantage."),
        p("<b>Plugin Architecture:</b> The platform must support a plugin system that allows third-party developers to extend platform capabilities without modifying core code. Plugins must run in a sandboxed environment with restricted access to platform resources. The plugin API must provide access to core platform capabilities including AI interaction, memory retrieval, knowledge base search, and workflow execution. Plugins must declare their required permissions explicitly, and users must approve permissions before installation. The plugin lifecycle, including installation, activation, deactivation, and uninstallation, must be manageable without platform downtime."),
        p("<b>API-First Design:</b> Every platform capability must be exposed through a versioned REST API before it is available in the user interface. The API must follow consistent design principles including resource-oriented URLs, standard HTTP methods, pagination, filtering, and sorting. API versioning must follow a deprecation policy that provides at least six months of advance notice before removing any endpoint. Rate limiting must be enforced per tenant with configurable limits. The API must support both synchronous request-response and asynchronous event-driven patterns."),
        p("<b>Webhook System:</b> The platform must support outbound webhooks that notify external systems of platform events, including workflow completion, agent status changes, document ingestion completion, and user-defined triggers. Webhooks must support configurable retry policies with exponential backoff. Webhook payloads must be signed using HMAC-SHA256 for authentication. The system must maintain a delivery log with status tracking and manual replay capability."),
        p("<b>Third-Party Integration Framework:</b> The platform must provide pre-built integrations with common enterprise tools including Slack, Microsoft Teams, Jira, GitHub, GitLab, Salesforce, and Google Workspace. Each integration must be available as a managed plugin that receives updates independently of the core platform. The integration framework must provide common patterns for authentication, data synchronization, event handling, and error reporting to reduce the development effort for new integrations."),
    ]

def section_28_accessibility_requirements():
    return add_major_section("28. Accessibility Requirements") + [
        p("Accessibility requirements ensure that Moataz AI is usable by people with disabilities, complying with legal obligations and expanding the platform's addressable user base. Accessibility is not an afterthought; it is a design constraint that must be validated from the earliest prototypes."),
        p("<b>WCAG Compliance:</b> The web application must meet WCAG 2.1 Level AA standards at launch. This includes all four principles: perceivable, operable, understandable, and robust. Specific requirements include: text alternatives for all non-text content, captions for audio content, content adaptable to different presentation formats without losing information, distinguishable content with sufficient color contrast ratios of at least 4.5:1 for normal text and 3:1 for large text, keyboard accessibility for all interactive elements, sufficient time for users to read and interact with content, content that does not cause seizures through flashing animations, and navigable content with clear wayfinding and consistent layout."),
        p("<b>Screen Reader Support:</b> The platform must be fully operable with major screen readers including JAWS, NVDA, and VoiceOver. All interactive elements must have appropriate ARIA labels and roles. Dynamic content updates must be announced through ARIA live regions. The workspace layout must be navigable through structured headings and landmarks. The chat interface must provide a linear navigation mode for screen reader users who cannot navigate the spatial layout."),
        p("<b>Keyboard Navigation:</b> All platform features must be accessible through keyboard navigation without requiring a mouse. Focus indicators must be clearly visible with a minimum contrast ratio of 3:1. Focus order must follow a logical sequence that matches the visual layout. Keyboard shortcuts must be provided for common actions and must be discoverable through a help overlay. No keyboard traps must exist; users must always be able to navigate away from any element using standard keyboard commands."),
        p("<b>Inclusive Design Principles:</b> The platform must support user preferences for reduced motion, high contrast, and enlarged text. Font sizes must be configurable with a minimum supported size of 200% of the default without loss of content or functionality. Color must never be the sole means of conveying information; all color-coded elements must have additional indicators such as icons or text labels. Error messages must be descriptive and must suggest corrections, not merely state that an error occurred."),
    ]

def section_29_internationalization_requirements():
    return add_major_section("29. Internationalization Requirements") + [
        p("Internationalization requirements ensure that Moataz AI can serve users across different languages, cultures, and regions. As a global enterprise platform, internationalization is not a future consideration but a launch requirement that must be embedded in the architecture from the beginning."),
        p("<b>Language Support:</b> The platform must support a minimum of twelve languages at launch, including English, Arabic, Chinese (Simplified and Traditional), French, German, Japanese, Korean, Portuguese, Spanish, Hindi, and Russian. The user interface, error messages, documentation, and onboarding flows must be fully translated for each supported language. The platform must support right-to-left layout for Arabic and Hebrew, including mirrored navigation, reversed text direction, and culturally appropriate iconography. Users must be able to switch languages without reloading the application, and language preference must persist across sessions."),
        p("<b>Content Localization:</b> AI interactions must respect the user's language preference. When a user communicates in a language other than English, the AI must respond in the same language with native-level fluency. The knowledge base must support documents in multiple languages with language-aware search that returns results in the query language regardless of the document's original language. Date, time, number, and currency formatting must follow the user's locale settings. Time zones must be handled correctly for all timestamp displays, including scheduling, audit logs, and collaboration features."),
        p("<b>Cultural Adaptation:</b> The platform must avoid culturally specific imagery, metaphors, or references that may be inappropriate or confusing in certain regions. Color schemes must be reviewed for cultural associations; for example, red implies danger in Western cultures but prosperity in some Asian cultures. Iconography must be reviewed for cultural sensitivity across all supported regions. Default content and examples must be globally appropriate rather than region-specific."),
        p("<b>Data Residency:</b> The platform architecture must support data residency requirements for all regions where the platform operates. Each tenant must be able to specify the geographic region where their data is stored and processed. Data must never leave the designated region without explicit tenant configuration, including backups and disaster recovery replicas. The system must provide documentation and tooling for tenants to verify that their data residency requirements are being met."),
    ]

def section_30_risk_analysis():
    return add_major_section("30. Risk Analysis") + [
        p("Risk analysis provides a structured assessment of the threats to the platform's success, organized by category and evaluated by severity and likelihood. Each risk is assigned a composite risk score that drives prioritization of mitigation efforts."),
    ] + make_table(
        [
            [Paragraph('<b>Risk Category</b>', table_header_style),
             Paragraph('<b>Risk Description</b>', table_header_style),
             Paragraph('<b>Severity</b>', table_header_style),
             Paragraph('<b>Likelihood</b>', table_header_style),
             Paragraph('<b>Risk Score</b>', table_header_style)],
            [Paragraph('Technical', table_cell_style),
             Paragraph('AI provider API breaking changes disrupt platform', table_cell_style),
             Paragraph('High', table_cell_center),
             Paragraph('Medium', table_cell_center),
             Paragraph('High', table_cell_center)],
            [Paragraph('Technical', table_cell_style),
             Paragraph('Multi-tenant data leakage vulnerability', table_cell_style),
             Paragraph('Critical', table_cell_center),
             Paragraph('Low', table_cell_center),
             Paragraph('High', table_cell_center)],
            [Paragraph('Technical', table_cell_style),
             Paragraph('Memory system performance degradation at scale', table_cell_style),
             Paragraph('High', table_cell_center),
             Paragraph('Medium', table_cell_center),
             Paragraph('High', table_cell_center)],
            [Paragraph('Market', table_cell_style),
             Paragraph('Major AI provider launches competing platform', table_cell_style),
             Paragraph('Critical', table_cell_center),
             Paragraph('Medium', table_cell_center),
             Paragraph('Critical', table_cell_center)],
            [Paragraph('Market', table_cell_style),
             Paragraph('Enterprise adoption slower than projected', table_cell_style),
             Paragraph('High', table_cell_center),
             Paragraph('Medium', table_cell_center),
             Paragraph('High', table_cell_center)],
            [Paragraph('Operational', table_cell_style),
             Paragraph('Talent acquisition difficulty for specialized AI roles', table_cell_style),
             Paragraph('Medium', table_cell_center),
             Paragraph('High', table_cell_center),
             Paragraph('High', table_cell_center)],
            [Paragraph('Regulatory', table_cell_style),
             Paragraph('New AI regulations impose unexpected compliance costs', table_cell_style),
             Paragraph('High', table_cell_center),
             Paragraph('Medium', table_cell_center),
             Paragraph('High', table_cell_center)],
            [Paragraph('Strategic', table_cell_style),
             Paragraph('Scope creep from enterprise custom requirements', table_cell_style),
             Paragraph('Medium', table_cell_center),
             Paragraph('High', table_cell_center),
             Paragraph('High', table_cell_center)],
        ],
        [AVAILABLE_WIDTH * 0.13, AVAILABLE_WIDTH * 0.42, AVAILABLE_WIDTH * 0.12, AVAILABLE_WIDTH * 0.13, AVAILABLE_WIDTH * 0.12],
        "Table 5: Risk Analysis Matrix"
    )

def section_31_project_assumptions():
    return add_major_section("31. Project Assumptions") + [
        p("Project assumptions are the conditions that must hold true for the engineering plan to be valid. Each assumption is stated with its justification and the consequences if it proves false."),
        p("<b>Market Assumptions:</b> The enterprise AI market will continue growing at or above current projections of 35-40% CAGR through 2028. If growth slows significantly, the addressable market may not support the platform's revenue targets, requiring a pivot toward mid-market or SMB segments. Enterprises will continue adopting multi-provider AI strategies rather than consolidating on a single provider. If the market consolidates around one dominant provider, the provider-agnostic value proposition weakens, though it does not disappear because compliance and cost optimization will still drive multi-provider adoption. The regulatory environment will become more complex, not less, creating demand for compliance-aware AI platforms."),
        p("<b>Technology Assumptions:</b> AI model APIs will remain accessible through HTTP-based interfaces with streaming support. If providers move to proprietary protocols, the AI Gateway abstraction layer must be adapted. AI model costs will continue to decrease on a per-token basis, following the historical trend. If costs increase due to provider market power or regulatory requirements, the cost optimization value proposition becomes even more compelling. Latency for cloud-based AI inference will remain below two seconds for standard requests. If latency increases due to model complexity or provider throttling, the platform may need to invest in edge deployment or local model execution."),
        p("<b>Team Assumptions:</b> The engineering team can be assembled with the required expertise in distributed systems, AI integration, security engineering, and front-end development within the first quarter. If talent acquisition is slower than planned, the launch timeline must be adjusted rather than compromising on team quality. The team will follow agile development practices with two-week sprint cycles and continuous deployment. If organizational pressures lead to waterfall practices, the platform's ability to iterate based on user feedback will be compromised."),
        p("<b>Infrastructure Assumptions:</b> Cloud infrastructure costs will follow current pricing trends with modest annual reductions. If cloud costs increase unexpectedly, the unit economics of the SaaS model must be recalculated. The platform can achieve the required performance and reliability targets on a single cloud provider initially, with multi-cloud support added post-launch. If enterprise customers demand multi-cloud from day one, the architecture must be adapted with corresponding timeline and cost implications."),
    ]

def section_32_project_constraints():
    return add_major_section("32. Project Constraints") + [
        p("Project constraints are the hard boundaries within which the platform must be built. Unlike assumptions, constraints are non-negotiable limits that cannot be changed through engineering effort alone."),
        p("<b>Budget Constraints:</b> The initial development budget must support the engineering team, cloud infrastructure, AI provider API costs, and third-party services for the first eighteen months before the platform generates sufficient revenue to be self-sustaining. AI provider API costs are a variable expense that scales with usage; the architecture must implement cost controls including token budget enforcement, model selection optimization, and caching strategies to manage this cost line."),
        p("<b>Timeline Constraints:</b> The platform must achieve a minimum viable product launch within twelve months of development start. This timeline is driven by market dynamics: the window for establishing a new AI platform is narrowing as major providers build out their own integrated offerings. The twelve-month timeline allows for three months of architectural design and infrastructure setup, six months of core module development, and three months of integration testing, performance optimization, and security hardening."),
        p("<b>Technology Constraints:</b> The platform must be built on cloud-native infrastructure that supports global deployment. The primary deployment target is a major cloud provider, with the architecture designed to be cloud-agnostic for future multi-cloud support. The web application must support the latest two major versions of Chrome, Firefox, Safari, and Edge. The Android application must support Android 10 and above. The platform must not depend on any technology that cannot be replaced without architectural changes, avoiding lock-in to specific databases, message queues, or AI frameworks."),
        p("<b>Regulatory Constraints:</b> The platform must comply with GDPR from launch, including data subject access requests, right to erasure, and data portability. The platform must not process, store, or transmit data in ways that violate the AI regulations of any jurisdiction where it operates. The platform must maintain the ability to respond to legal process, including data preservation requests and court orders, while protecting user privacy to the maximum extent permitted by law."),
    ]

def section_33_technical_challenges():
    return add_major_section("33. Technical Challenges") + [
        p("Technical challenges are the engineering problems that require novel or particularly complex solutions. They represent the areas of highest technical risk and the opportunities for the greatest competitive differentiation."),
        p("<b>Multi-Provider AI Orchestration:</b> Orchestrating AI requests across multiple providers with different API schemas, tokenization schemes, streaming behaviors, rate limits, and error modes is fundamentally more complex than integrating with a single provider. The challenge is not merely routing requests but doing so intelligently: selecting the optimal provider for each request based on capability requirements, latency targets, cost constraints, data residency policies, and current provider health. The system must also normalize the differences between providers, so that upstream modules do not need to be aware of which provider is handling a given request. This requires building an abstraction layer that is simultaneously flexible enough to accommodate provider-specific features and stable enough to provide a consistent interface to the rest of the platform."),
        p("<b>Memory System Consistency at Scale:</b> The memory system must provide consistent, low-latency retrieval across millions of memory entries while maintaining strict multi-tenant isolation. The challenge is that memory retrieval is fundamentally a vector similarity search operation, which does not naturally align with traditional database isolation models. The system must ensure that a query from one tenant never retrieves memories from another tenant, even in the presence of software bugs or hardware failures. Additionally, the memory system must handle concurrent reads and writes from thousands of users without consistency anomalies, such as a user reading a memory that is in the process of being updated by another operation."),
        p("<b>Sandbox Security:</b> The sandbox execution environment must run arbitrary user-generated code without compromising the security of the host system or other tenants. This requires container-level isolation with strict resource limits, network policies that prevent outbound connections except to explicitly whitelisted endpoints, filesystem isolation that prevents access to the host filesystem, and process isolation that prevents privilege escalation. The challenge is that each of these isolation layers introduces performance overhead, and the sandbox must still provide sub-five-second cold start times and responsive execution. The tension between security and performance is the core engineering challenge."),
        p("<b>Real-Time Collaboration at Scale:</b> The team collaboration features require real-time synchronization of workspace state across multiple concurrent users. The challenge is implementing conflict resolution for simultaneous edits to shared resources, including documents, workflows, and AI interaction contexts. Operational transformation and CRDT-based approaches each have tradeoffs in terms of consistency, latency, and implementation complexity. The chosen approach must scale to support large teams and must handle edge cases such as network partitions, device failures, and offline editing."),
    ]

def section_34_potential_risks():
    return add_major_section("34. Potential Risks") + [
        p("This section provides deep-dive analysis of specific risk scenarios, including root cause analysis, impact assessment, and early warning indicators that enable proactive mitigation before the risk materializes."),
        p("<b>Risk: AI Provider Pricing Shock.</b> Scenario: One or more AI providers dramatically increase pricing, making the platform's cost structure unsustainable at current subscription rates. Root cause: Provider market consolidation or provider strategy to capture more value from platform companies. Impact: Direct impact on unit economics; if AI costs exceed subscription revenue, the platform operates at a loss. Early warning: Provider pricing announcements, changes in API terms of service, and industry analyst reports on provider pricing trends. Mitigation: Maintain relationships with multiple providers, invest in self-hosted model capabilities for cost-sensitive workloads, and design subscription pricing with provider cost pass-through mechanisms."),
        p("<b>Risk: Multi-Tenant Data Breach.</b> Scenario: A software vulnerability allows one tenant to access another tenant's data. Root cause: Authentication or authorization bypass, SQL injection, or misconfigured data isolation. Impact: Catastrophic for customer trust, potentially triggering regulatory investigations and litigation. Early warning: Security audit findings, penetration test results, and anomalous access patterns detected by monitoring systems. Mitigation: Defense-in-depth with multiple isolation layers, mandatory security reviews for all data access code, regular penetration testing, and bug bounty program."),
        p("<b>Risk: Competitive Platform Launch by Major Provider.</b> Scenario: OpenAI, Google, or Anthropic launches an integrated platform that replicates many of Moataz AI's features. Root cause: Providers expanding up the value chain from model APIs to end-user platforms. Impact: Significant competitive pressure on the platform's differentiation. Early warning: Provider product announcements, job postings for platform engineering roles, and patent filings. Mitigation: Deepen integration breadth faster than any single provider can match, leverage provider-agnostic neutrality as a trust differentiator, and build ecosystem network effects through the plugin marketplace that create switching costs independent of any single provider's platform."),
        p("<b>Risk: Regulatory Compliance Overload.</b> Scenario: New AI regulations in major markets impose compliance requirements that were not anticipated in the original architecture. Root cause: Rapidly evolving regulatory landscape for AI, particularly in the EU, US, and China. Impact: Significant engineering effort diverted to compliance, potentially delaying feature development. Early warning: Legislative proposals, regulatory agency announcements, and industry association alerts. Mitigation: Design compliance architecture to be extensible from the start, participate in industry standards bodies, and maintain relationships with regulatory counsel in all target markets."),
    ]

def section_35_mitigation_strategies():
    return add_major_section("35. Mitigation Strategies") + [
        p("Mitigation strategies define concrete actions to reduce the likelihood or impact of identified risks. Each strategy is evaluated for cost-benefit tradeoff and implementation priority."),
        p("<b>Technical Risk Mitigation:</b> For AI provider dependencies, the primary mitigation is the provider-agnostic architecture itself, which enables rapid provider switching. Secondary mitigations include maintaining abstraction layers that isolate provider-specific code, implementing comprehensive integration tests that validate each provider independently, and establishing relationships with provider technical teams for advance notice of API changes. For memory system scalability, the mitigation strategy is to design the storage architecture with pluggable backends, enabling migration from one vector database to another without application-level changes. For sandbox security, the mitigation is defense-in-depth with multiple independent isolation layers, regular security audits, and a bug bounty program."),
        p("<b>Market Risk Mitigation:</b> For competitive pressure from major providers, the mitigation strategy is to build ecosystem depth faster than any single provider can replicate. This means investing heavily in the plugin marketplace, the agent ecosystem, and the workflow engine, all of which create network effects that compound over time. A single provider can replicate features but not ecosystem. For enterprise adoption risk, the mitigation is a land-and-expand strategy that starts with individual users and small teams, building organizational champions who advocate for enterprise-wide deployment."),
        p("<b>Operational Risk Mitigation:</b> For talent acquisition challenges, the mitigation strategy is to invest in employer branding, offer competitive compensation, and build a distributed team that can hire from a global talent pool. For scope creep, the mitigation is a rigorous prioritization framework that classifies every feature request by its impact on the core value proposition and its cost in engineering time. Features that do not directly strengthen the platform's integration advantage are deferred."),
        p("<b>Regulatory Risk Mitigation:</b> For regulatory uncertainty, the mitigation strategy is to design the compliance architecture to be extensible rather than specific. Rather than implementing compliance for a specific regulation, the platform implements compliance primitives, such as data residency enforcement, audit logging, and consent management, that can be composed to meet any regulatory requirement. This approach reduces the cost of adapting to new regulations and positions the platform as a compliance-enabling tool rather than a compliance-consuming one."),
    ]

def section_36_success_metrics():
    return add_major_section("36. Success Metrics") + [
        p("Success metrics define the key performance indicators and objectives and key results that measure the platform's progress toward its goals. These metrics are organized by category and include both leading indicators that predict future performance and lagging indicators that confirm achieved results."),
    ] + make_table(
        [
            [Paragraph('<b>Category</b>', table_header_style),
             Paragraph('<b>Metric</b>', table_header_style),
             Paragraph('<b>Target (Year 1)</b>', table_header_style),
             Paragraph('<b>Measurement</b>', table_header_style)],
            [Paragraph('Adoption', table_cell_style),
             Paragraph('Monthly Active Users', table_cell_style),
             Paragraph('50,000 MAU', table_cell_center),
             Paragraph('Unique users with 1+ AI interaction per month', table_cell_style)],
            [Paragraph('Adoption', table_cell_style),
             Paragraph('Enterprise Tenants', table_cell_style),
             Paragraph('500+ tenants', table_cell_center),
             Paragraph('Active enterprise subscriptions', table_cell_style)],
            [Paragraph('Engagement', table_cell_style),
             Paragraph('Daily Active / Monthly Active', table_cell_style),
             Paragraph('DAU/MAU > 40%', table_cell_center),
             Paragraph('Ratio of daily to monthly active users', table_cell_style)],
            [Paragraph('Engagement', table_cell_style),
             Paragraph('AI Interactions per User per Day', table_cell_style),
             Paragraph('> 10 interactions', table_cell_center),
             Paragraph('Average AI interactions per active user per day', table_cell_style)],
            [Paragraph('Retention', table_cell_style),
             Paragraph('30-Day Retention', table_cell_style),
             Paragraph('> 70%', table_cell_center),
             Paragraph('Users active 30 days after signup', table_cell_style)],
            [Paragraph('Retention', table_cell_style),
             Paragraph('Enterprise Churn Rate', table_cell_style),
             Paragraph('< 5% monthly', table_cell_center),
             Paragraph('Enterprise subscription cancellations', table_cell_style)],
            [Paragraph('Performance', table_cell_style),
             Paragraph('AI Response Latency (p95)', table_cell_style),
             Paragraph('< 2,000ms', table_cell_center),
             Paragraph('95th percentile end-to-end response time', table_cell_style)],
            [Paragraph('Performance', table_cell_style),
             Paragraph('Platform Uptime', table_cell_style),
             Paragraph('> 99.95%', table_cell_center),
             Paragraph('Rolling monthly availability', table_cell_style)],
            [Paragraph('Business', table_cell_style),
             Paragraph('Annual Recurring Revenue', table_cell_style),
             Paragraph('$1M+ ARR', table_cell_center),
             Paragraph('Annualized subscription revenue', table_cell_style)],
            [Paragraph('Ecosystem', table_cell_style),
             Paragraph('Plugin Marketplace Listings', table_cell_style),
             Paragraph('50+ plugins', table_cell_center),
             Paragraph('Published and actively maintained plugins', table_cell_style)],
        ],
        [AVAILABLE_WIDTH * 0.13, AVAILABLE_WIDTH * 0.25, AVAILABLE_WIDTH * 0.18, AVAILABLE_WIDTH * 0.44],
        "Table 6: Success Metrics and Year-One Targets"
    )

def section_37_acceptance_criteria():
    return add_major_section("37. Acceptance Criteria") + [
        p("Acceptance criteria define the testable conditions that must be met before the platform can be considered ready for each deployment phase. These criteria serve as the quality gate between development and release."),
        p("<b>MVP Launch Acceptance Criteria:</b> The AI Gateway must successfully route requests to at least four distinct AI providers with automatic failover. The Memory System must persist and retrieve context across sessions for at least 1,000 concurrent users. The Knowledge Base must ingest and enable semantic search over documents in PDF, DOCX, and Markdown formats. The Workspace must persist state across browser sessions with automatic recovery. The team collaboration features must support at least 25 concurrent users in a shared workspace with real-time synchronization. Authentication must support email/password and at least two enterprise SSO providers. Multi-tenant isolation must be verified through penetration testing with no cross-tenant access vulnerabilities. The platform must pass a comprehensive security audit with no critical or high-severity findings."),
        p("<b>General Availability Acceptance Criteria:</b> All MVP criteria must continue to pass at ten times the load. The platform must support at least 10,000 concurrent users with performance targets met. The plugin system must support at least 20 third-party plugins. The workflow engine must support workflows with at least 50 steps and conditional branching. The Android application must be available on Google Play with a 4.0+ star rating. The platform must achieve SOC 2 Type II readiness with all required controls implemented and documented. Disaster recovery procedures must be tested through at least two simulated regional outage exercises. The API must be documented with OpenAPI specifications and contract tests covering all endpoints."),
        p("<b>Enterprise Readiness Acceptance Criteria:</b> The platform must support at least 100,000 concurrent users with performance targets met. Data residency must be enforced across at least three geographic regions. The compliance architecture must support GDPR, including data subject access requests completed within 30 days and right-to-erasure executed within 72 hours. Enterprise SSO must support SAML 2.0 and OpenID Connect with automatic user provisioning and deprovisioning. The platform must maintain complete audit logs for all AI interactions, data access events, and administrative actions with log retention of at least seven years. The platform must achieve ISO 27001 certification readiness."),
    ]

def section_38_future_expansion():
    return add_major_section("38. Future Expansion Strategy") + [
        p("The future expansion strategy defines the roadmap for growing the platform beyond its initial launch capabilities, covering new modules, geographic markets, vertical solutions, and ecosystem partnerships over a five-year horizon."),
        p("<b>Module Expansion (Years 1-2):</b> Following the core module launch, the platform will expand with the Desktop Application, enabling deeper OS integration and offline capabilities. The Advanced Agent Marketplace will be introduced, creating a self-sustaining ecosystem of third-party AI agents. Enhanced analytics and reporting capabilities will provide enterprises with deeper insights into AI usage patterns, cost allocation, and productivity impact. The Voice AI module will be expanded to support real-time voice conversations with AI, enabling hands-free operation for mobile and accessibility use cases."),
        p("<b>Geographic Expansion (Years 1-3):</b> Launch in North America and Europe will be followed by expansion into the Middle East and North Africa, leveraging the Arabic language support built into the platform from day one. Asia-Pacific expansion will follow, with localized deployments in Japan, South Korea, and Southeast Asia. Each geographic expansion requires not just data residency infrastructure but also compliance with local regulations, partnership with local cloud providers, and culturally appropriate user experience adaptations."),
        p("<b>Vertical Solutions (Years 2-4):</b> The platform will develop industry-specific solutions that leverage its compliance architecture and customizable agent platform. Healthcare solutions will include HIPAA-compliant workflows, clinical documentation assistance, and medical literature analysis. Financial services solutions will include regulatory compliance monitoring, risk assessment automation, and financial report generation. Legal solutions will include contract analysis, legal research assistance, and compliance checklist automation. Each vertical solution will be developed in partnership with domain experts and will include pre-built agents, workflows, and knowledge base templates."),
        p("<b>Ecosystem Partnerships (Years 2-5):</b> The platform will establish partnerships with major enterprise software vendors to build native integrations, with cloud providers to offer marketplace listing and co-selling arrangements, with system integrators to offer implementation services, and with AI research institutions to provide early access to cutting-edge capabilities. These partnerships create a go-to-market multiplier that accelerates adoption beyond what the core team could achieve alone."),
    ]

def section_39_development_philosophy():
    return add_major_section("39. Recommended Development Philosophy") + [
        p("The development philosophy defines the engineering culture and practices that will govern how the platform is built. For a platform of this scale and ambition, the philosophy is not incidental; it is a strategic choice that determines whether the team can sustain velocity, quality, and innovation over a multi-year development cycle."),
        p("<b>Iterative Delivery:</b> The platform will be developed through iterative delivery cycles with working software shipped to production every two weeks. Each iteration must deliver user-visible value, not just internal infrastructure. This practice ensures that the team receives real user feedback on a continuous basis, that the architecture evolves based on actual usage patterns rather than speculative design, and that the platform is always in a deployable state. The iterative approach requires discipline in managing technical debt, with explicit capacity allocation for refactoring and infrastructure improvement within each sprint."),
        p("<b>Test-First Development:</b> All production code must be developed with test-first practices. Unit tests must be written before implementation code. Integration tests must be defined before service interfaces are finalized. End-to-end tests must be defined before user stories are considered complete. The test-first approach is not merely about catching bugs; it is about driving design toward testable, modular architectures. Code that is difficult to test is code that is difficult to maintain, and the test-first discipline forces the team to confront design problems early rather than deferring them."),
        p("<b>Observability-Driven Development:</b> Every feature must be instrumented with metrics, logs, and traces before it is deployed to production. The team must define success criteria in terms of observable behavior, such as latency percentiles, error rates, and user engagement metrics, rather than functional correctness alone. Observability-driven development enables the team to detect problems before users report them, to diagnose issues in production without reproducing them locally, and to make data-driven decisions about feature prioritization based on actual usage patterns."),
        p("<b>Documentation-as-Code:</b> All documentation must be version-controlled alongside the code it describes. Architectural decision records must be written for every significant technical choice. API documentation must be generated from code annotations and must be automatically validated for accuracy. Runbooks must be tested through game day exercises and must be updated immediately when procedures change. The documentation-as-code philosophy ensures that documentation is always current and that the cost of maintaining documentation is proportional to the cost of maintaining the code."),
        p("<b>Blameless Post-Mortems:</b> Every production incident must be followed by a blameless post-mortem within 48 hours. The post-mortem must identify the root cause, the contributing factors, and the specific actions to prevent recurrence. The goal is systemic improvement, not individual blame. The team must foster a culture where engineers feel safe reporting mistakes, because the fastest path to reliability is through honest, rapid identification of failure modes."),
    ]

def section_40_engineering_principles():
    return add_major_section("40. Engineering Principles") + [
        p("Engineering principles are the concrete rules that govern every technical decision. Unlike the core philosophy, which provides directional guidance, engineering principles are prescriptive constraints that must be explicitly validated during design reviews and architectural decision records."),
        p("<b>API-First Design:</b> Every capability must be exposed through a versioned API before it is available in any user interface. This principle ensures that all platform features are programmatically accessible, enabling automation, integration, and the plugin ecosystem. It also forces the team to design clean service boundaries because an API is a contract that cannot be easily changed after consumers depend on it."),
        p("<b>Stateless Services:</b> Application services must be stateless, with all persistent state delegated to dedicated data stores. This principle enables horizontal scaling by allowing any service instance to handle any request, supports blue-green deployments by eliminating session affinity, and simplifies disaster recovery by reducing the amount of state that must be replicated."),
        p("<b>Event-Driven Architecture:</b> Services must communicate through asynchronous events for cross-service operations, using synchronous requests only for direct user-facing queries. This principle decouples services, enabling independent deployment and scaling. It also provides a natural audit trail, since events represent a chronological record of all system activities. The event backbone must support at-least-once delivery with idempotent consumers to ensure reliability."),
        p("<b>Defense in Depth:</b> Security controls must be implemented at every layer: network, application, data, and user. No single control should be considered sufficient to prevent unauthorized access. This principle requires that even if one layer is compromised, the remaining layers continue to protect the system. Practical implementations include network segmentation, application-layer encryption, database-level access controls, and user-level audit logging."),
        p("<b>Graceful Degradation:</b> The system must degrade gracefully under load or partial failure, maintaining core functionality even when non-essential features are unavailable. When an AI provider experiences an outage, the system must automatically route to alternative providers. When the memory system is under heavy load, the system must continue to serve AI requests without memory context rather than failing entirely. When a non-critical service fails, the system must continue operating with reduced functionality and must clearly communicate the degraded state to users."),
        p("<b>Explicit Over Implicit:</b> All behavior must be explicitly defined and documented. Magic, such as implicit state transitions, auto-detected configurations, or undocumented side effects, is forbidden. This principle reduces the cognitive load on developers who must understand and modify the system, and it eliminates an entire category of bugs caused by unexpected interactions between implicit behaviors."),
        p("<b>Fail Loudly:</b> When the system encounters an unexpected condition, it must fail loudly with clear error messages and diagnostic information, rather than silently degrading or producing incorrect results. Silent failures are the most dangerous class of bugs because they can persist for extended periods before detection. Loud failures enable rapid diagnosis and resolution."),
        p("<b>Evolutionary Architecture:</b> The architecture must be designed to evolve over time rather than requiring periodic rewrites. This principle requires implementing architectural fitness functions that measure whether the system maintains its required architectural characteristics as it grows. It also requires building abstraction layers at integration points that enable the replacement of underlying technologies without affecting upstream consumers. The goal is an architecture that can adapt to changing requirements and technology landscapes without the disruption and risk of a complete rewrite."),
    ]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PRE-FLIGHT CHECKLIST (Section before final)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def section_preflight_checklist():
    """Final checklist that must be completed before moving to Prompt 02."""
    checklist_items = [
        "Product vision, mission, and philosophy are fully documented and reviewed",
        "All 19 major platform features are cataloged with purpose and expected behavior",
        "Core modules for MVP are identified with dependencies mapped",
        "Future modules are defined with timeline estimates and prerequisites",
        "Functional requirements are enumerated with priority classification (P0/P1/P2)",
        "Non-functional requirements are defined with measurable acceptance criteria",
        "Security requirements address authentication, authorization, encryption, and compliance",
        "Performance targets are established with percentiles and measurement methods",
        "Availability and reliability SLAs are defined with disaster recovery procedures",
        "Scalability model supports growth from 1,000 to 100,000+ concurrent users",
        "Risk analysis is complete with severity, likelihood, and mitigation strategies",
        "User personas are defined with specific scenarios and success metrics",
        "Success metrics and KPIs are established with year-one targets",
        "Acceptance criteria for MVP, GA, and enterprise readiness are defined",
        "Internationalization requirements cover 12+ languages and data residency",
        "Accessibility requirements target WCAG 2.1 Level AA compliance",
        "Development philosophy and engineering principles are documented and agreed upon",
        "Project assumptions and constraints are identified with contingency plans",
        "Technical challenges are analyzed with proposed solution approaches",
        "All stakeholders have reviewed and approved this engineering foundation document",
    ]
    elements = add_major_section("Pre-Flight Checklist for Prompt 02") + [
        p("The following checklist must be completed in its entirety before proceeding to Prompt 02, which will address system architecture, technology selection, and implementation planning. Each item represents a gate that ensures the product understanding is sufficiently complete to inform architectural decisions. No item should be marked complete based on assumption; each requires explicit validation through review, research, or stakeholder confirmation."),
    ]
    for i, item in enumerate(checklist_items, 1):
        elements.append(Paragraph(f"[ ] {i}. {item}", body_style))
    elements.append(Spacer(1, 24))
    elements.append(callout("This document is the engineering foundation. Every subsequent development phase, architectural decision, and implementation sprint will reference this artifact. Its completeness and accuracy are non-negotiable prerequisites for the success of the Moataz AI platform."))
    return elements


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# BUILD DOCUMENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT_DIR = '/home/z/my-project/download'
BODY_PDF = os.path.join(OUTPUT_DIR, 'moataz_blueprint_body.pdf')

doc = TocDocTemplate(
    BODY_PDF,
    pagesize=A4,
    leftMargin=LEFT_MARGIN,
    rightMargin=RIGHT_MARGIN,
    topMargin=TOP_MARGIN,
    bottomMargin=BOTTOM_MARGIN,
    title="Moataz AI Platform Engineering Blueprint",
    author="Z.ai",
    creator="Z.ai",
    subject="Prompt 01 — Product Vision, Master Analysis & Engineering Foundation"
)

story = []

# ── TABLE OF CONTENTS ──
story.append(Paragraph("<b>Table of Contents</b>", ParagraphStyle(
    name='TOCTitle', fontName='FreeSerif-Bold', fontSize=20, leading=28,
    spaceBefore=12, spaceAfter=18, textColor=HEADER_FILL, alignment=TA_LEFT
)))
toc = TableOfContents()
toc.levelStyles = [toc_level0, toc_level1]
story.append(toc)
story.append(PageBreak())

# ── ADD ALL 40 SECTIONS ──
all_sections = [
    section_01_executive_summary,
    section_02_vision_statement,
    section_03_mission_statement,
    section_04_core_philosophy,
    section_05_primary_objectives,
    section_06_business_goals,
    section_07_technical_goals,
    section_08_user_goals,
    section_09_long_term_vision,
    section_10_unique_selling_points,
    section_11_competitive_advantages,
    section_12_target_users,
    section_13_user_personas,
    section_14_problems,
    section_15_user_journey,
    section_16_major_features,
    section_17_core_modules,
    section_18_future_modules,
    section_19_functional_requirements,
    section_20_nonfunctional_requirements,
    section_21_security_requirements,
    section_22_performance_requirements,
    section_23_availability_requirements,
    section_24_scalability_requirements,
    section_25_maintainability_requirements,
    section_26_reliability_requirements,
    section_27_extensibility_requirements,
    section_28_accessibility_requirements,
    section_29_internationalization_requirements,
    section_30_risk_analysis,
    section_31_project_assumptions,
    section_32_project_constraints,
    section_33_technical_challenges,
    section_34_potential_risks,
    section_35_mitigation_strategies,
    section_36_success_metrics,
    section_37_acceptance_criteria,
    section_38_future_expansion,
    section_39_development_philosophy,
    section_40_engineering_principles,
]

for section_func in all_sections:
    story.extend(section_func())

# ── PRE-FLIGHT CHECKLIST ──
story.extend(section_preflight_checklist())

# ── BUILD ──
print("Building body PDF with Table of Contents...")
doc.multiBuild(story)
print(f"Body PDF generated: {BODY_PDF}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GENERATE COVER PAGE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COVER_HTML = os.path.join(OUTPUT_DIR, 'moataz_blueprint_cover.html')
COVER_PDF = os.path.join(OUTPUT_DIR, 'moataz_blueprint_cover.pdf')

cover_html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&family=Playfair+Display:wght@400;700;900&display=swap" rel="stylesheet">
  <style>
    @page { size: 794px 1123px; margin: 0; }
    :root {
      --c-bg: #f4f5f5;
      --c-accent: #297ca6;
      --c-text: #171819;
      --c-muted: #848a8d;
      --c-mid: #344e5b;
      --c-surface: #ebeeef;
    }
    html, body {
      margin: 0; padding: 0;
      width: 794px; height: 1123px;
      background: var(--c-bg);
      color: var(--c-text);
      font-family: 'Inter', sans-serif;
    }
    @media screen {
      html { height: auto; display: flex; justify-content: center; min-height: 100vh; background: var(--c-bg); }
      body { transform-origin: top center; scale: min(1, calc(100vw / 794), calc(100vh / 1123)); margin: 0 auto; box-shadow: 0 0 60px rgba(0,0,0,0.15); }
    }
    .cover {
      width: 794px; height: 1123px; position: relative;
      box-sizing: border-box;
    }
    /* Layer 1: Background - Grid pattern */
    .bg-layer {
      position: absolute; inset: 0; overflow: hidden; z-index: 1;
    }
    .bg-grid {
      position: absolute; inset: 0;
      background-image:
        linear-gradient(var(--c-accent) 1px, transparent 1px),
        linear-gradient(90deg, var(--c-accent) 1px, transparent 1px);
      background-size: 50px 50px;
      opacity: 0.03;
    }
    /* Layer 2: Structure - Anchor line */
    .struct-layer {
      position: absolute; inset: 0; z-index: 2;
    }
    .vline {
      position: absolute;
      left: 95px; top: 112px; bottom: 112px;
      width: 6px;
      background: var(--c-mid);
    }
    /* Layer 3: Content */
    .content-layer {
      position: absolute; inset: 0; z-index: 3;
    }
    .kicker {
      position: absolute; top: 168px; left: 140px;
      font-size: 12pt; font-weight: 400;
      letter-spacing: 3px; text-transform: uppercase;
      color: var(--c-muted); opacity: 0.7;
    }
    .title {
      position: absolute; top: 336px; left: 140px;
      font-size: 48pt; font-weight: 900;
      line-height: 1.1; color: var(--c-mid);
      font-family: 'Inter', sans-serif;
      max-width: 560px;
    }
    .title .accent {
      color: var(--c-accent);
    }
    .summary {
      position: absolute; top: 560px; left: 140px;
      font-size: 14pt; font-weight: 400;
      line-height: 1.6; color: var(--c-text);
      opacity: 0.75; max-width: 480px;
    }
    .meta {
      position: absolute; top: 760px; left: 140px;
      font-size: 13pt; font-weight: 400;
      line-height: 1.8; color: var(--c-muted);
    }
    .meta .label {
      font-size: 9pt; letter-spacing: 2px;
      text-transform: uppercase; color: var(--c-accent);
      display: block; margin-bottom: 2px;
    }
    .footer {
      position: absolute; bottom: 90px; left: 140px; right: 95px;
      font-size: 10pt; color: var(--c-muted); opacity: 0.5;
      letter-spacing: 1px;
    }
  </style>
</head>
<body>
  <div class="cover">
    <div class="bg-layer">
      <div class="bg-grid"></div>
    </div>
    <div class="struct-layer">
      <div class="vline"></div>
    </div>
    <div class="content-layer">
      <div class="kicker">Engineering Blueprint  |  Prompt 01</div>
      <div class="title">MOATAZ<br><span class="accent">AI</span></div>
      <div class="summary">Product Vision, Master Analysis & Engineering Foundation for the next-generation AI Operating System. A comprehensive engineering blueprint covering vision, requirements, risks, and strategic direction before architecture design begins.</div>
      <div class="meta">
        <span class="label">Classification</span>
        Confidential  |  Engineering Foundation<br>
        <span class="label">Scope</span>
        19 Modules  |  Global Enterprise SaaS  |  Provider-Agnostic<br>
        <span class="label">Document Version</span>
        1.0  |  June 2026
      </div>
      <div class="footer">MOATAZ AI PLATFORM ENGINEERING BLUEPRINT  |  CONFIDENTIAL</div>
    </div>
  </div>
</body>
</html>"""

with open(COVER_HTML, 'w', encoding='utf-8') as f:
    f.write(cover_html_content)
print(f"Cover HTML generated: {COVER_HTML}")

# Render cover to PDF
import subprocess
scripts_dir = os.path.join(PDF_SKILL_DIR, 'scripts')
result = subprocess.run(
    ['node', os.path.join(scripts_dir, 'html2poster.js'),
     COVER_HTML, '--output', COVER_PDF, '--width', '794px'],
    capture_output=True, text=True
)
if result.returncode != 0:
    print(f"Cover rendering error: {result.stderr}")
else:
    print(f"Cover PDF generated: {COVER_PDF}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MERGE COVER + BODY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from pypdf import PdfReader, PdfWriter

FINAL_PDF = os.path.join(OUTPUT_DIR, 'Moataz_AI_Engineering_Blueprint.pdf')

A4_W, A4_H = 595.28, 841.89

def normalize_page_to_a4(page):
    """Always normalize to exact A4 dimensions."""
    page.scale_to(A4_W, A4_H)
    return page

writer = PdfWriter()

# Cover as page 1
if os.path.exists(COVER_PDF):
    cover_page = PdfReader(COVER_PDF).pages[0]
    writer.add_page(normalize_page_to_a4(cover_page))
    print("Cover page added.")
else:
    print("WARNING: Cover PDF not found, skipping cover.")

# Body pages follow
for page in PdfReader(BODY_PDF).pages:
    writer.add_page(normalize_page_to_a4(page))

writer.add_metadata({
    '/Title': 'Moataz AI Platform Engineering Blueprint',
    '/Author': 'Z.ai',
    '/Creator': 'Z.ai',
    '/Subject': 'Prompt 01 - Product Vision, Master Analysis & Engineering Foundation',
})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ADD PAGE NUMBERS VIA REPORTLAB + PYPDF OVERLAY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from reportlab.pdfgen import canvas as pdfcanvas
from io import BytesIO

def create_page_number_pdf(page_num):
    """Create a single-page PDF with just the page number."""
    buf = BytesIO()
    c = pdfcanvas.Canvas(buf, pagesize=A4)
    c.setFont('FreeSerif', 9)
    c.setFillColor(TEXT_MUTED)
    c.drawCentredString(A4_W / 2.0, 32, f"{page_num}")
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]

# Add page numbers to body pages (skip cover page = index 0, skip TOC = index 1)
# Body pages start at index 2 in the writer
total_pages = len(writer.pages)
for i in range(1, total_pages):  # Skip cover page (index 0), start numbering from page 2
    page_num = i  # Page 2 = "1", page 3 = "2", etc. (but TOC is page 2, so we show i)
    stamp_page = create_page_number_pdf(page_num)
    writer.pages[i].merge_page(stamp_page)

print("Page numbers added to all body pages.")

with open(FINAL_PDF, 'wb') as f:
    writer.write(f)

print(f"\n{'='*60}")
print(f"FINAL PDF DELIVERED: {FINAL_PDF}")
print(f"{'='*60}")

# Cleanup temp files
for tmp in [BODY_PDF, COVER_PDF, COVER_HTML]:
    if os.path.exists(tmp):
        os.remove(tmp)
        print(f"Cleaned up: {tmp}")
