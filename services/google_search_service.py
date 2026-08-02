import os
import requests

# ===== OPENSTAX MATERIALS DATABASE =====
OPENSTAX_MATERIALS = {
    # Biology
    'BIO101': [
        {
            'title': 'Biology 2e - Introduction to Biology',
            'url': 'https://openstax.org/books/biology-2e/pages/1-introduction',
            'description': 'Comprehensive introduction to biological sciences'
        },
        {
            'title': 'Biology 2e - Chemistry of Life',
            'url': 'https://openstax.org/books/biology-2e/pages/2-introduction',
            'description': 'Chemical foundations of biology'
        },
        {
            'title': 'Biology 2e - Cell Structure and Function',
            'url': 'https://openstax.org/books/biology-2e/pages/3-introduction',
            'description': 'Understanding cellular organization'
        }
    ],
    'BIO102': [
        {
            'title': 'Biology 2e - Genetics',
            'url': 'https://openstax.org/books/biology-2e/pages/11-introduction',
            'description': 'Principles of heredity and genetic variation'
        },
        {
            'title': 'Biology 2e - Evolution and Diversity',
            'url': 'https://openstax.org/books/biology-2e/pages/18-introduction',
            'description': 'Theory of evolution and biological diversity'
        }
    ],
    'BIO201': [
        {
            'title': 'Biology 2e - Animal Structure and Function',
            'url': 'https://openstax.org/books/biology-2e/pages/33-introduction',
            'description': 'Anatomy and physiology of animals'
        }
    ],
    'BIO203': [
        {
            'title': 'Biology 2e - Genetics',
            'url': 'https://openstax.org/books/biology-2e/pages/11-introduction',
            'description': 'Introductory genetics principles'
        }
    ],

    # Chemistry
    'CHM101': [
        {
            'title': 'Chemistry 2e - Essential Ideas',
            'url': 'https://openstax.org/books/chemistry-2e/pages/1-introduction',
            'description': 'Fundamental concepts in chemistry'
        },
        {
            'title': 'Chemistry 2e - Atoms, Molecules, and Ions',
            'url': 'https://openstax.org/books/chemistry-2e/pages/2-introduction',
            'description': 'Basic chemical composition and structure'
        },
        {
            'title': 'Chemistry 2e - Stoichiometry',
            'url': 'https://openstax.org/books/chemistry-2e/pages/4-introduction',
            'description': 'Chemical calculations and reactions'
        }
    ],
    'CHM102': [
        {
            'title': 'Chemistry 2e - Thermochemistry',
            'url': 'https://openstax.org/books/chemistry-2e/pages/5-introduction',
            'description': 'Energy changes in chemical reactions'
        },
        {
            'title': 'Chemistry 2e - Electronic Structure',
            'url': 'https://openstax.org/books/chemistry-2e/pages/6-introduction',
            'description': 'Atomic structure and electron configuration'
        }
    ],
    'CHM201': [
        {
            'title': 'Chemistry 2e - Chemical Bonding',
            'url': 'https://openstax.org/books/chemistry-2e/pages/7-introduction',
            'description': 'Ionic and covalent bonding principles'
        }
    ],
    'CHM205': [
        {
            'title': 'Chemistry 2e - Gases',
            'url': 'https://openstax.org/books/chemistry-2e/pages/9-introduction',
            'description': 'Gas laws and kinetic molecular theory'
        }
    ],

    # Physics
    'PHY101': [
        {
            'title': 'University Physics Vol 1 - Mechanics',
            'url': 'https://openstax.org/books/university-physics-volume-1/pages/1-introduction',
            'description': 'Introduction to classical mechanics'
        },
        {
            'title': 'University Physics Vol 1 - Motion Along a Straight Line',
            'url': 'https://openstax.org/books/university-physics-volume-1/pages/3-introduction',
            'description': 'Kinematics in one dimension'
        },
        {
            'title': 'University Physics Vol 1 - Forces and Newton\'s Laws',
            'url': 'https://openstax.org/books/university-physics-volume-1/pages/5-introduction',
            'description': 'Newton\'s laws of motion'
        }
    ],
    'PHY102': [
        {
            'title': 'University Physics Vol 1 - Work and Energy',
            'url': 'https://openstax.org/books/university-physics-volume-1/pages/7-introduction',
            'description': 'Energy conservation and work-energy theorem'
        },
        {
            'title': 'University Physics Vol 2 - Electric Charges and Fields',
            'url': 'https://openstax.org/books/university-physics-volume-2/pages/5-introduction',
            'description': 'Introduction to electrostatics'
        }
    ],
    'PHY201': [
        {
            'title': 'University Physics Vol 2 - Current and Resistance',
            'url': 'https://openstax.org/books/university-physics-volume-2/pages/9-introduction',
            'description': 'Electric current and circuit analysis'
        }
    ],

    # Mathematics
    'MTH101': [
        {
            'title': 'College Algebra - Prerequisites',
            'url': 'https://openstax.org/books/college-algebra-2e/pages/1-introduction-to-prerequisites',
            'description': 'Algebraic foundations'
        },
        {
            'title': 'College Algebra - Equations and Inequalities',
            'url': 'https://openstax.org/books/college-algebra-2e/pages/2-introduction-to-equations-and-inequalities',
            'description': 'Solving equations and inequalities'
        }
    ],
    'MTH102': [
        {
            'title': 'College Algebra - Functions',
            'url': 'https://openstax.org/books/college-algebra-2e/pages/3-introduction-to-functions',
            'description': 'Introduction to functions and graphs'
        },
        {
            'title': 'Calculus Vol 1 - Functions and Graphs',
            'url': 'https://openstax.org/books/calculus-volume-1/pages/1-introduction',
            'description': 'Preparation for calculus'
        }
    ],
    'MTH201': [
        {
            'title': 'Calculus Vol 1 - Limits',
            'url': 'https://openstax.org/books/calculus-volume-1/pages/2-introduction',
            'description': 'Introduction to limits and continuity'
        },
        {
            'title': 'Calculus Vol 1 - Derivatives',
            'url': 'https://openstax.org/books/calculus-volume-1/pages/3-introduction',
            'description': 'Differential calculus fundamentals'
        }
    ],
    'MTH202': [
        {
            'title': 'Calculus Vol 1 - Integration',
            'url': 'https://openstax.org/books/calculus-volume-1/pages/5-introduction',
            'description': 'Integral calculus and applications'
        }
    ],

    # Biochemistry
    'BCH201': [
        {
            'title': 'Biology 2e - Biological Macromolecules',
            'url': 'https://openstax.org/books/biology-2e/pages/3-introduction',
            'description': 'Proteins, carbohydrates, lipids, and nucleic acids'
        },
        {
            'title': 'Chemistry 2e - Organic Chemistry',
            'url': 'https://openstax.org/books/chemistry-2e/pages/20-introduction',
            'description': 'Introduction to organic chemistry'
        }
    ],
    'BCH202': [
        {
            'title': 'Biology 2e - Metabolism',
            'url': 'https://openstax.org/books/biology-2e/pages/7-introduction',
            'description': 'Cellular metabolism and energy'
        }
    ],

    # Computer Science
    'CSC101': [
        {
            'title': 'Introduction to Python Programming',
            'url': 'https://openstax.org/books/introduction-python-programming/pages/1-introduction',
            'description': 'Python programming fundamentals'
        }
    ],
    'CSC102': [
        {
            'title': 'Introduction to Python Programming - Data Structures',
            'url': 'https://openstax.org/books/introduction-python-programming/pages/6-introduction',
            'description': 'Python data structures and algorithms'
        }
    ],

    # Statistics
    'STA112': [
        {
            'title': 'Introductory Statistics - Sampling and Data',
            'url': 'https://openstax.org/books/introductory-statistics/pages/1-introduction',
            'description': 'Statistical data collection and analysis'
        },
        {
            'title': 'Introductory Statistics - Probability',
            'url': 'https://openstax.org/books/introductory-statistics/pages/3-introduction',
            'description': 'Probability theory fundamentals'
        }
    ],
    'STA211': [
        {
            'title': 'Introductory Statistics - Discrete Random Variables',
            'url': 'https://openstax.org/books/introductory-statistics/pages/4-introduction',
            'description': 'Discrete probability distributions'
        }
    ],

    # Microbiology
    'MCB101': [
        {
            'title': 'Microbiology - Introduction to Microbiology',
            'url': 'https://openstax.org/books/microbiology/pages/1-introduction',
            'description': 'Fundamentals of microbiology'
        }
    ],
    'MCB201': [
        {
            'title': 'Microbiology - Microbial Metabolism',
            'url': 'https://openstax.org/books/microbiology/pages/8-introduction',
            'description': 'Bacterial metabolism and energy production'
        }
    ],

    # Accounting
    'ACC101': [
        {
            'title': 'Principles of Accounting Vol 1 - Financial Accounting',
            'url': 'https://openstax.org/books/principles-financial-accounting/pages/1-why-it-matters',
            'description': 'Introduction to financial accounting'
        }
    ],
    'ACC201': [
        {
            'title': 'Principles of Managerial Accounting',
            'url': 'https://openstax.org/books/principles-managerial-accounting/pages/1-why-it-matters',
            'description': 'Management accounting principles'
        }
    ],

    # Business
    'BUS101': [
        {
            'title': 'Introduction to Business',
            'url': 'https://openstax.org/books/introduction-business/pages/1-introduction',
            'description': 'Business fundamentals and organization'
        }
    ],
    'BUS201': [
        {
            'title': 'Principles of Management',
            'url': 'https://openstax.org/books/principles-management/pages/1-introduction',
            'description': 'Management theory and practice'
        }
    ],

    # Economics
    'ECO101': [
        {
            'title': 'Principles of Economics 2e - Introduction',
            'url': 'https://openstax.org/books/principles-economics-2e/pages/1-introduction',
            'description': 'Economic principles and theory'
        }
    ],
    'ECO201': [
        {
            'title': 'Principles of Microeconomics 2e',
            'url': 'https://openstax.org/books/principles-microeconomics-2e/pages/1-introduction',
            'description': 'Microeconomic analysis'
        }
    ],

    # GST/GNS general-studies courses — these repeat across nearly every department's
    # 100-level curriculum, so covering them here has outsized reach even though each
    # individual entry only maps to one code. Every URL below was checked live and loads.
    'GST101': [
        {
            'title': 'Writing Guide with Handbook - Introduction',
            'url': 'https://openstax.org/books/writing-guide/pages/1-introduction',
            'description': 'Academic writing fundamentals and composition'
        }
    ],
    'GST111': [
        {
            'title': 'Writing Guide with Handbook - Introduction',
            'url': 'https://openstax.org/books/writing-guide/pages/1-introduction',
            'description': 'Academic writing fundamentals and composition'
        }
    ],
    'GST122': [
        {
            'title': 'Writing Guide with Handbook - Rhetorical Situations',
            'url': 'https://openstax.org/books/writing-guide/pages/2-introduction',
            'description': 'Purpose, audience, and structure in writing'
        }
    ],
    'GST112': [
        {
            'title': 'Introduction to Philosophy - What Philosophy Is',
            'url': 'https://openstax.org/books/introduction-philosophy/pages/1-introduction',
            'description': 'Logic, reasoning, and philosophical inquiry'
        }
    ],
    'GST212': [
        {
            'title': 'Introduction to Python Programming',
            'url': 'https://openstax.org/books/introduction-python-programming/pages/1-introduction',
            'description': 'Fundamentals of using computers and programming'
        }
    ],
    'GST223': [
        {
            'title': 'Entrepreneurship - Entrepreneurship Today',
            'url': 'https://openstax.org/books/entrepreneurship/pages/1-introduction',
            'description': 'Introduction to entrepreneurial thinking'
        },
        {
            'title': 'Entrepreneurship - Entrepreneurial Vision and Goals',
            'url': 'https://openstax.org/books/entrepreneurship/pages/2-introduction',
            'description': 'Setting goals and vision as an entrepreneur'
        }
    ],
    'GST224': [
        {
            'title': 'Principles of Management - Introduction',
            'url': 'https://openstax.org/books/principles-management/pages/1-introduction',
            'description': 'Leadership and management fundamentals'
        }
    ],
    'GST311': [
        {
            'title': 'Entrepreneurship - Entrepreneurship Today',
            'url': 'https://openstax.org/books/entrepreneurship/pages/1-introduction',
            'description': 'Introduction to entrepreneurial thinking'
        },
        {
            'title': 'Entrepreneurship - Entrepreneurial Vision and Goals',
            'url': 'https://openstax.org/books/entrepreneurship/pages/2-introduction',
            'description': 'Setting goals and vision as an entrepreneur'
        }
    ],

    # Entrepreneurship (ENT) — distinct department code prefix, same real book.
    'ENT211': [
        {
            'title': 'Entrepreneurship - Entrepreneurship Today',
            'url': 'https://openstax.org/books/entrepreneurship/pages/1-introduction',
            'description': 'Introduction to entrepreneurial thinking'
        },
        {
            'title': 'Entrepreneurship - Entrepreneurial Vision and Goals',
            'url': 'https://openstax.org/books/entrepreneurship/pages/2-introduction',
            'description': 'Setting goals and vision as an entrepreneur'
        }
    ],
    'ENT321': [
        {
            'title': 'Entrepreneurship - Entrepreneurship Today',
            'url': 'https://openstax.org/books/entrepreneurship/pages/1-introduction',
            'description': 'Entrepreneurship and business management foundations'
        },
        {
            'title': 'Entrepreneurship - Entrepreneurial Vision and Goals',
            'url': 'https://openstax.org/books/entrepreneurship/pages/2-introduction',
            'description': 'Business planning and entrepreneurial goal-setting'
        }
    ],
    'ENT421': [
        {
            'title': 'Entrepreneurship - Entrepreneurship Today',
            'url': 'https://openstax.org/books/entrepreneurship/pages/1-introduction',
            'description': 'General entrepreneurship foundation (not investment-specific — no free OER exists yet for investment marketing specifically)'
        }
    ],

    # Mathematics under the "MAT" prefix (same content as MTH101 under a different
    # department's course-code convention).
    'MAT101': [
        {
            'title': 'College Algebra - Prerequisites',
            'url': 'https://openstax.org/books/college-algebra-2e/pages/1-introduction-to-prerequisites',
            'description': 'Algebraic foundations'
        },
        {
            'title': 'College Algebra - Equations and Inequalities',
            'url': 'https://openstax.org/books/college-algebra-2e/pages/2-introduction-to-equations-and-inequalities',
            'description': 'Solving equations and inequalities'
        }
    ],

    # Experimental Physics — measurement/units content applies across both semesters.
    'PHY107': [
        {
            'title': 'University Physics Vol 1 - Units and Standards',
            'url': 'https://openstax.org/books/university-physics-volume-1/pages/1-2-units-and-standards',
            'description': 'Measurement, units, and experimental precision'
        },
        {
            'title': 'University Physics Vol 1 - Mechanics',
            'url': 'https://openstax.org/books/university-physics-volume-1/pages/1-introduction',
            'description': 'Foundations for mechanics lab work'
        }
    ],
    'PHY108': [
        {
            'title': 'University Physics Vol 1 - Units and Standards',
            'url': 'https://openstax.org/books/university-physics-volume-1/pages/1-2-units-and-standards',
            'description': 'Measurement, units, and experimental precision'
        },
        {
            'title': 'University Physics Vol 2 - Electric Charges and Fields',
            'url': 'https://openstax.org/books/university-physics-volume-2/pages/5-introduction',
            'description': 'Foundations for electricity/electromagnetism lab work'
        }
    ]
}

GOOGLE_API_KEY = os.environ.get('GOOGLE_CUSTOM_SEARCH_API_KEY')
GOOGLE_SEARCH_ENGINE_ID = os.environ.get('GOOGLE_SEARCH_ENGINE_ID')


def search_google_pdfs(course_code, max_results=10):
    """
    Search Google Custom Search API for PDF materials related to a course code.

    Returns (results, api_ok):
      - results: list of dicts with title, url, snippet (possibly empty)
      - api_ok: False if the API itself failed (bad key, quota, not enabled, network
        error) — as opposed to the API working fine but genuinely having no results.
        Callers use this to tell students "search is down right now" instead of the
        misleading "no materials found for this course" when it's actually our key.
    """
    if not GOOGLE_API_KEY or not GOOGLE_SEARCH_ENGINE_ID:
        print("[WARNING] Google API credentials not configured")
        return [], False

    # Try multiple query variations for better results
    queries = [
        f'{course_code} lecture notes filetype:pdf',
        f'{course_code} past questions filetype:pdf',
        f'{course_code} study material filetype:pdf'
    ]

    all_results = []
    seen_urls = set()
    api_ok = True

    for query in queries[:2]:  # Limit to 2 queries to stay within free tier
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': GOOGLE_API_KEY,
                'cx': GOOGLE_SEARCH_ENGINE_ID,
                'q': query,
                'num': min(max_results, 10),
                'fileType': 'pdf'
            }

            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])

                for item in items:
                    pdf_url = item.get('link', '')
                    if pdf_url and pdf_url not in seen_urls:
                        seen_urls.add(pdf_url)
                        all_results.append({
                            'title': item.get('title', f'{course_code} Material'),
                            'url': pdf_url,
                            'snippet': item.get('snippet', '')
                        })
            else:
                api_ok = False
                print(f"[ERROR] Google API error: {response.status_code} - {response.text[:200]}")

        except Exception as e:
            api_ok = False
            print(f"[ERROR] Google search exception: {str(e)}")
            continue

    return all_results[:max_results], api_ok
