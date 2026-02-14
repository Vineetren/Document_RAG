# AI Development Notes

## AI Tools Used During Development

### Amazon Q Developer
Used Amazon Q extensively throughout the development process for:

#### Code Generation (80% AI-assisted)
- **Backend Structure**: FastAPI routes, database models, service layer architecture
- **Frontend Components**: HTML templates, JavaScript functions, CSS styling
- **Integration Logic**: ChromaDB setup, OpenAI API integration, session management
- **Error Handling**: Exception handling, validation logic, edge case management

#### Code Review & Debugging (90% AI-assisted)
- **Bug Fixes**: TypeError fixes, parameter mismatches, CSS issues
- **Code Optimization**: Refactoring for better structure and maintainability
- **Best Practices**: Security considerations, proper error handling patterns

#### Feature Implementation (85% AI-assisted)
- **Authentication System**: Session-based auth with middleware
- **User Isolation**: Per-user documents and chat history
- **Theme System**: Light/dark mode with localStorage persistence
- **Smart Filtering**: Source relevance filtering and snippet extraction
- **Status Monitoring**: Health check system for backend, DB, and LLM

### What I Checked/Validated Myself

#### Manual Testing (100% Manual)
- Login/logout flow with different credentials
- Document upload with various file types and sizes
- Question answering accuracy and relevance
- Source citation correctness
- Theme switching across pages
- Chat history persistence
- User isolation verification
- Status page accuracy

#### Configuration & Setup (100% Manual)
- Environment variable configuration
- API key setup and testing
- Database initialization and migration
- Directory structure organization
- Dependency management

#### Design Decisions (70% Manual, 30% AI-suggested)
- UI/UX layout and color scheme
- Database schema design
- API endpoint structure
- Error message wording
- Feature prioritization

#### Security Review (60% Manual, 40% AI-assisted)
- Session security validation
- SQL injection prevention verification
- File upload validation
- User data isolation testing
- API endpoint protection

## LLM Provider & Model Choice

### Provider: OpenRouter
**Why OpenRouter?**
- **Cost-effective**: Significantly cheaper than direct OpenAI API
- **Flexibility**: Easy to switch between different models
- **Reliability**: Good uptime and performance
- **Compatibility**: OpenAI-compatible API format

### Models Used

#### 1. Embeddings: `text-embedding-3-small`
**Why this model?**
- **Cost**: Very affordable at $0.02 per 1M tokens
- **Performance**: Good quality embeddings for semantic search
- **Speed**: Fast embedding generation
- **Dimension**: 1536 dimensions, good balance of quality and size

#### 2. Chat Completions: `meta-llama/llama-3.1-8b-instruct` (configurable)
**Why Llama 3.1 8B Instruct?**
- **Cost**: Free on OpenRouter (or very low cost)
- **Quality**: Good instruction following for document Q&A
- **Speed**: Fast response times with 8B parameters
- **Open Source**: Meta's open-source model, widely available
- **Context Window**: 128K tokens, sufficient for document chunks
- **Instruction Tuned**: Specifically trained to follow instructions

**Alternative Models Considered:**
- GPT-4o-mini: Better quality but costs money
- GPT-4: Too expensive for this use case
- GPT-3.5-turbo: Similar cost, lower quality than Llama 3.1
- Claude models: Good quality but more expensive
- Smaller Llama models: Lower quality for complex reasoning

### Prompt Engineering

#### Iterative Refinement (AI-assisted)
The LLM prompt went through several iterations:
1. Basic instruction prompt
2. Added greeting detection
3. Added off-topic redirection
4. Added edge case handling (single items, missing info)
5. Added response tagging for source filtering

**Final Prompt Strategy:**
- Clear numbered rules for different scenarios
- Explicit examples for edge cases
- Response tagging system ([CASUAL] vs [DOCUMENT])
- Natural language instructions for better compliance

## Development Workflow

### Typical Feature Development Process
1. **Requirement Discussion**: Clarify feature with user
2. **AI Code Generation**: Use Amazon Q to generate initial code
3. **Manual Review**: Check logic, security, and edge cases
4. **Testing**: Manual testing of functionality
5. **Iteration**: Fix bugs and refine based on testing
6. **Integration**: Ensure feature works with existing code

### Code Quality Assurance
- **AI-generated code**: Always reviewed for security and correctness
- **Database queries**: Manually verified for SQL injection safety
- **API endpoints**: Tested with various inputs and edge cases
- **Frontend logic**: Tested across different browsers and themes

## Lessons Learned

### What Worked Well
- AI excellent at boilerplate and repetitive code
- AI helpful for debugging specific errors
- AI good at suggesting best practices
- Iterative refinement with AI feedback

### What Required Manual Intervention
- Complex business logic decisions
- Security considerations
- User experience fine-tuning
- Performance optimization
- Database migration strategy

## Conclusion

AI tools (specifically Amazon Q) significantly accelerated development, handling ~80% of code generation and ~90% of debugging. However, critical thinking, testing, and validation remained essential manual tasks. The combination of AI assistance and human oversight resulted in a robust, secure, and user-friendly application.
