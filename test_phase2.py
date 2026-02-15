"""
Phase 2 Testing Script
Test all AI services without needing the full API
"""

import json
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_concept_extractor():
    """Test concept extraction"""
    print("\n" + "="*60)
    print("1️⃣  TESTING CONCEPT EXTRACTOR")
    print("="*60)
    
    try:
        from services.concept_extractor import ConceptExtractor
        
        extractor = ConceptExtractor()
        
        sample_text = """
        Photosynthesis is a biochemical process that converts light energy from 
        the sun into chemical energy stored in glucose. It takes place in the 
        chloroplasts of plant cells and involves two main stages: 
        light-dependent reactions and the Calvin cycle.
        """
        
        print("\n📝 Input Text:")
        print(sample_text)
        
        print("\n🔄 Extracting concepts...")
        result = extractor.extract_concepts(sample_text)
        
        print(f"\n✅ Extracted {len(result.get('concepts', []))} concepts:")
        for concept in result.get('concepts', [])[:3]:
            print(f"   • {concept.get('name')} (importance: {concept.get('importance')})")
        
        print("\n🔗 Mapping relationships...")
        relationships = extractor.map_relationships(result.get('concepts', []))
        
        print(f"✅ Found {len(relationships.get('edges', []))} relationships")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_workflow_generator():
    """Test workflow generation"""
    print("\n" + "="*60)
    print("2️⃣  TESTING WORKFLOW GENERATOR")
    print("="*60)
    
    try:
        from services.workflow_generator import WorkflowGenerator
        
        generator = WorkflowGenerator()
        
        sample_texts = [
            "Understanding the basic principles of photosynthesis and how plants use sunlight.",
            "The light reactions that occur in the thylakoid membranes produce ATP and NADPH.",
            "The Calvin cycle uses ATP and NADPH to fix CO2 into glucose molecules."
        ]
        
        print(f"\n📝 Input: {len(sample_texts)} text segments")
        
        print("\n🔄 Generating workflow...")
        workflow = generator.generate_workflow(sample_texts)
        
        print(f"\n✅ Generated {len(workflow['steps'])} learning steps:")
        
        for step in workflow['steps']:
            deps_text = f" (depends on: {step['dependencies']})" if step['dependencies'] else ""
            print(f"   {step['order'] + 1}. {step['title']}{deps_text}")
        
        print(f"\n📊 Total concepts: {workflow.get('conceptCount', 0)}")
        print(f"📊 Relationships: {len(workflow.get('relationships', []))}")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_summary_generator():
    """Test summary generation"""
    print("\n" + "="*60)
    print("3️⃣  TESTING SUMMARY GENERATOR")
    print("="*60)
    
    try:
        from services.summary_generator import SummaryGenerator
        
        generator = SummaryGenerator()
        
        step_content = """
        Photosynthesis is a biochemical process in which light energy is converted 
        into chemical energy. The light-dependent reactions occur in the thylakoid 
        membranes where chlorophyll absorbs photons. Electrons are excited and move 
        through electron transport chains, generating ATP and NADPH. These products 
        are then used in the light-independent reactions (Calvin cycle) to fix CO2 
        into glucose.
        """
        
        print("\n📝 Input: Step 1 of 5 - Introduction to Photosynthesis")
        
        print("\n🔄 Generating summary...")
        summary = generator.generate_summary(
            step_title="Light Reactions in Photosynthesis",
            step_content=step_content,
            step_number=1,
            total_steps=5,
            language="English"
        )
        
        if summary.get('success'):
            print(f"\n✅ Generated Summary:")
            print(f"\n{summary.get('summary', 'No summary')[:300]}...")
            
            print(f"\n🎯 Key Points:")
            for point in summary.get('keyPoints', [])[:3]:
                print(f"   • {point}")
            
            print(f"\n📚 Difficulty: {summary.get('difficulty', 'Unknown')}")
            print(f"🌍 Language: {summary.get('language', 'Unknown')}")
            
            return True
        else:
            print("❌ Summary generation failed")
            return False
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    print("\n" + "="*60)
    print("📦 CHECKING DEPENDENCIES")
    print("="*60)
    
    required = ['fastapi', 'uvicorn', 'pydantic', 'dotenv']
    optional = ['langchain', 'google.generativeai', 'networkx']
    
    print("\n🔴 Core Dependencies:")
    all_core_ok = True
    for pkg in required:
        try:
            __import__(pkg.replace('-', '_').split('.')[0])
            print(f"   ✅ {pkg}")
        except ImportError:
            print(f"   ❌ {pkg} - Missing")
            all_core_ok = False
    
    print("\n🟡 AI Dependencies (Optional):")
    for pkg in optional:
        try:
            __import__(pkg.replace('-', '_').split('.')[0])
            print(f"   ✅ {pkg}")
        except ImportError:
            print(f"   ⚠️  {pkg} - Not installed (using fallback mode)")
    
    if not all_core_ok:
        print("\n⚠️  Install missing core packages:")
        print("   python -m pip install fastapi uvicorn python-dotenv pydantic")
    
    return all_core_ok

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 PHASE 2 - AI SERVICES TEST SUITE")
    print("="*60)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Missing core dependencies. Cannot proceed.")
        return False
    
    print("\n⏳ Running tests...\n")
    
    results = {
        "Concept Extractor": test_concept_extractor(),
        "Workflow Generator": test_workflow_generator(),
        "Summary Generator": test_summary_generator()
    }
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST RESULTS SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {name}")
    
    print(f"\n📈 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ Phase 2 AI Services are working perfectly!")
        print("\nNext steps:")
        print("  1. Integrate these services into api/main.py")
        print("  2. Create new endpoints for AI-powered workflow generation")
        print("  3. Test with actual PDF uploads from your React frontend")
    else:
        print("\n⚠️  Some tests failed. Check error messages above.")
        print("\nTroubleshooting:")
        print("  • Install missing packages: python -m pip install -r requirements.txt")
        print("  • Check .env file: GOOGLE_API_KEY must be configured")
        print("  • Restart Python to reload modules")
    
    print("\n" + "="*60 + "\n")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
