import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import './LandingPage.css'
import mx_logo from '../assets/mx-logo.png'

// ── Icons ──────────────────────────────────────────────────────────────────
const QRIcon = ({ size = 22 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
    <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
    <rect x="5" y="5" width="3" height="3" fill="currentColor" stroke="none"/>
    <rect x="16" y="5" width="3" height="3" fill="currentColor" stroke="none"/>
    <rect x="16" y="16" width="3" height="3" fill="currentColor" stroke="none"/>
    <rect x="5" y="16" width="3" height="3" fill="currentColor" stroke="none"/>
  </svg>
)

const LeafIcon = ({ size = 22 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z"/>
    <path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>
  </svg>
)

const RecycleIcon = ({ size = 22 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="1 4 1 10 7 10"/><polyline points="23 20 23 14 17 14"/>
    <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"/>
  </svg>
)

const ChartIcon = ({ size = 22 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/>
    <line x1="6" y1="20" x2="6" y2="14"/><line x1="2" y1="20" x2="22" y2="20"/>
  </svg>
)

const PeopleIcon = ({ size = 26 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>
    <path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>
  </svg>
)

const TruckIcon = ({ size = 26 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <rect x="1" y="3" width="15" height="13"/>
    <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/>
    <circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>
  </svg>
)

const FactoryIcon = ({ size = 26 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2z"/>
    <path d="M17 18h1"/><path d="M12 18h1"/><path d="M7 18h1"/>
  </svg>
)

const BuildingIcon = ({ size = 26 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/>
  </svg>
)

const GlobeIcon = ({ size = 26 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/>
    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
  </svg>
)

const ArrowRight = ({ size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
  </svg>
)

const PlayIcon = () => (
  <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
)

const MenuIcon = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
    <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>
  </svg>
)

const CloseIcon = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
    <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
  </svg>
)

// ── Cycle Diagram ──────────────────────────────────────────────────────────
const CycleDiagram = () => {
  const dots = [
    [212,172],[232,182],[217,197],[242,202],[227,212],
    [202,187],[247,187],[222,222],[202,212],[232,167],
    [252,212],[207,227],[237,232],[222,242],[212,202],
    [197,177],[257,197],[242,222],[217,167],[202,197],
    [245,175],[198,240],[230,250],[260,200],[195,165],
  ]
  return (
    <div className="cycle-wrap">
      <svg className="cycle-svg" viewBox="0 0 440 440" fill="none">
        <defs>
          <marker id="arr" markerWidth="7" markerHeight="5" refX="6" refY="2.5" orient="auto">
            <polygon points="0 0,7 2.5,0 5" fill="#c9823a"/>
          </marker>
          <radialGradient id="ig" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#1a2a12"/>
            <stop offset="100%" stopColor="#0e1a0b"/>
          </radialGradient>
        </defs>
        <circle cx="220" cy="220" r="155" stroke="#4a7835" strokeWidth="1.5" strokeDasharray="5 6"/>
        <circle cx="220" cy="220" r="108" fill="url(#ig)" stroke="#2a3a20" strokeWidth="1"/>
        {dots.map(([x,y],i) => <circle key={i} cx={x} cy={y} r="2" fill="#6aaa50" opacity="0.45"/>)}
        <path d="M252 68A155 155 0 0 1 370 248" stroke="#c9823a" strokeWidth="1.8" markerEnd="url(#arr)"/>
        <path d="M370 252A155 155 0 0 1 252 372" stroke="#c9823a" strokeWidth="1.8" markerEnd="url(#arr)"/>
        <path d="M248 372A155 155 0 0 1 70 252" stroke="#c9823a" strokeWidth="1.8" markerEnd="url(#arr)"/>
        <path d="M70 248A155 155 0 0 1 248 68" stroke="#c9823a" strokeWidth="1.8" markerEnd="url(#arr)"/>
      </svg>
      <img src={mx_logo} className="cycle-logo" alt="MatXchange"/>
      <div className="cycle-node node-top">
        <div className="node-icon"><QRIcon size={18}/></div>
        <p className="node-title">TRACE</p>
        <p className="node-desc">Track waste<br/>from source</p>
      </div>
      <div className="cycle-node node-right">
        <div className="node-icon"><RecycleIcon size={18}/></div>
        <p className="node-title">VERIFY</p>
        <p className="node-desc">Verify data<br/>and assets</p>
      </div>
      <div className="cycle-node node-bottom">
        <div className="node-icon"><ChartIcon size={18}/></div>
        <p className="node-title">MEASURE</p>
        <p className="node-desc">Measure impact<br/>and performance</p>
      </div>
      <div className="cycle-node node-left">
        <div className="node-icon"><LeafIcon size={18}/></div>
        <p className="node-title">CONNECT</p>
        <p className="node-desc">Connect the<br/>waste economy</p>
      </div>
    </div>
  )
}

// ── Main Component ─────────────────────────────────────────────────────────
const LandingPage = () => {
  const [menuOpen, setMenuOpen] = useState(false)

  const scrollTo = (id) => {
    setMenuOpen(false)
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
  }

  const stakeholders = [
    { icon: <PeopleIcon/>,  title: 'For Collectors',    desc: 'Get recognized, earn more and grow your impact with instant M-Pesa payments for every verified collection.' },
    { icon: <TruckIcon/>,   title: 'For Aggregators',   desc: 'Streamline collection operations and ensure fully transparent, auditable reporting across all routes.' },
    { icon: <FactoryIcon/>, title: 'For Recyclers',     desc: 'Access verified materials with a traceable supply chain and reliable data from source to processing.' },
    { icon: <BuildingIcon/>,title: 'For Organizations', desc: 'Make data-driven ESG decisions, meet EPR obligations, and demonstrate verified environmental impact.' },
  ]

  const stats = [
    { icon: <LeafIcon size={30}/>,   value: '15,428+', label: 'Active Users',           sub: 'Collectors, aggregators & recyclers onboarded' },
    { icon: <RecycleIcon size={30}/>,value: '32,650+', label: 'Tons of Waste Tracked',  sub: 'Digitally verified and traceable across the system' },
    { icon: <ChartIcon size={30}/>,  value: '450+',    label: 'Partner Organizations',  sub: 'Working together for a cleaner, circular future' },
    { icon: <GlobeIcon size={30}/>,  value: '23',      label: 'Counties Reached',       sub: 'Building a nationwide circular economy network' },
  ]

  const steps = [
    { icon: <QRIcon size={20}/>,     num:'01', title:'Trace',   color:'#c9823a', desc:'Every kilogram of waste is logged at the point of collection — weighed, photographed, and recorded. Nothing enters the system unverified.' },
    { icon: <LeafIcon size={20}/>,   num:'02', title:'Connect', color:'#5a8040', desc:'Collectors, aggregators, recyclers, and producers are linked in one digital ecosystem. M-Pesa payments reach collectors the moment a transaction is confirmed.' },
    { icon: <RecycleIcon size={20}/>,num:'03', title:'Verify',  color:'#c9823a', desc:'Every transaction is anchored to the Stellar blockchain as a RECO token — one per kilogram collected. Tamper-proof, publicly auditable, and permanent.' },
    { icon: <ChartIcon size={20}/>,  num:'04', title:'Measure', color:'#5a8040', desc:'Real-time dashboards show kilograms collected, payouts made, tokens minted, and counties covered — giving every stakeholder live, verifiable impact data.' },
  ]

  return (
    <div className="landing">

      {/* Navbar */}
      <nav className="navbar">
        <div className="nav-inner">
          <img src={mx_logo} alt="MatXchange" className="nav-logo" onClick={() => scrollTo('home')}/>
          <div className={`nav-links ${menuOpen ? 'open' : ''}`}>
            <button onClick={() => scrollTo('how-it-works')}>Impact Estimator</button>
            <button onClick={() => scrollTo('solutions')}>Solutions</button>
            <button onClick={() => scrollTo('how-it-works')}>Verification</button>
            <button onClick={() => scrollTo('qr')}>Resources</button>
            <button onClick={() => scrollTo('about')}>About Us</button>
          </div>
          <div className="nav-actions">
            <Link to="/login" className="btn-login">Log In</Link>
            <button className="nav-menu-btn" onClick={() => setMenuOpen(v => !v)}>
              {menuOpen ? <CloseIcon/> : <MenuIcon/>}
            </button>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section id="home" className="hero">
        <div className="hero-inner">
          <div className="hero-left">
            <div className="hero-badge"><LeafIcon size={13}/><span>THE DIGITAL BACKBONE FOR CIRCULARITY</span></div>
            <h1 className="hero-title">
              Building the Traceability <span className="accent">System</span> for Kenya's Waste Economy.
            </h1>
            <p className="hero-sub">
              Connecting informal waste collectors, aggregators, and recyclers through a single, verifiable digital system.
            </p>
            <div className="hero-btns">
              <Link to="/login" className="btn-primary">Get Started <ArrowRight/></Link>
              <button className="btn-outline"><PlayIcon/> Watch Demo</button>
            </div>
            <div className="hero-values">
              {[
                { icon: <LeafIcon size={15}/>,   title: 'Transparent',   sub: 'End-to-end traceability' },
                { icon: <PeopleIcon size={15}/>, title: 'Inclusive',     sub: 'Empowering all players' },
                { icon: <ChartIcon size={15}/>,  title: 'Impact-Driven', sub: 'Real data. Real change.' },
              ].map((v,i) => (
                <div className="value-item" key={i}>
                  {v.icon}
                  <div>
                    <p className="val-title">{v.title}</p>
                    <p className="val-sub">{v.sub}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div className="hero-right"><CycleDiagram/></div>
        </div>
      </section>

      {/* Stakeholders */}
      <section id="solutions" className="section stakeholders-section">
        <div className="section-inner stake-grid">
          {stakeholders.map((s,i) => (
            <div className="stake-card" key={i}>
              <div className="stake-icon">{s.icon}</div>
              <h3>{s.title}</h3>
              <p>{s.desc}</p>
              <span className="card-arrow"><ArrowRight/></span>
            </div>
          ))}
        </div>
      </section>

      {/* Impact Stats */}
      <section className="section stats-section">
        <div className="section-inner stats-grid">
          {stats.map((s,i) => (
            <div className="stat-card" key={i}>
              <div className="stat-icon">{s.icon}</div>
              <p className="stat-value">{s.value}</p>
              <p className="stat-label">{s.label}</p>
              <p className="stat-sub">{s.sub}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="section howitworks-section">
        <div className="section-inner">
          <div className="section-header">
            <p className="section-tag">HOW IT WORKS</p>
            <h2>From Waste to Verified Impact</h2>
            <p className="section-sub">A single, end-to-end digital workflow connecting every player in Kenya's waste economy.</p>
          </div>
          <div className="steps-grid">
            {steps.map((s,i) => (
              <div className="step-card" key={i}>
                <span className="step-num" style={{color:s.color}}>{s.num}</span>
                <div className="step-icon" style={{color:s.color,background:`${s.color}18`}}>{s.icon}</div>
                <h3 style={{color:s.color}}>{s.title}</h3>
                <p>{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* QR Code Passports */}
      <section id="qr" className="section qr-section">
        <div className="section-inner qr-inner">
          <div className="qr-left">
            <p className="section-tag">PRODUCT PASSPORT</p>
            <h2>Every Product Tells Its Story</h2>
            <p className="qr-desc">
              Every item upcycled through MatXchange receives a unique QR code. Scan it to reveal the full verified journey — from the waste picker who collected the raw material, to the recycler who processed it, to the brand that made it something new.
            </p>
            <ul className="qr-features">
              <li><span className="check">✓</span> Collector name, location and date of collection</li>
              <li><span className="check">✓</span> Material type, weight and verified photo proof</li>
              <li><span className="check">✓</span> Recycler identity and processing method used</li>
              <li><span className="check">✓</span> Blockchain hash — publicly verifiable on Stellar</li>
              <li><span className="check">✓</span> RECO tokens minted per kilogram collected</li>
            </ul>
            <p className="qr-tagline">Turning every upcycled product into a verifiable sustainability story.</p>
          </div>
          <div className="qr-right">
            <div className="qr-card">
              <div className="qr-code-box">
                <svg width="76" height="76" viewBox="0 0 24 24" fill="none" stroke="#c9823a" strokeWidth="1.4">
                  <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
                  <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
                  <rect x="5" y="5" width="3" height="3" fill="#c9823a" stroke="none"/>
                  <rect x="16" y="5" width="3" height="3" fill="#c9823a" stroke="none"/>
                  <rect x="16" y="16" width="3" height="3" fill="#c9823a" stroke="none"/>
                  <rect x="5" y="16" width="3" height="3" fill="#c9823a" stroke="none"/>
                  <line x1="7" y1="12" x2="9" y2="12"/><line x1="12" y1="7" x2="12" y2="9"/>
                  <line x1="12" y1="14" x2="12" y2="17"/><line x1="14" y1="12" x2="17" y2="12"/>
                </svg>
                <p className="scan-label">Scan to view product history</p>
              </div>
              <div className="qr-story">
                {[
                  { dot:'orange', label:'Collected',          val:'1.2 kg Plastic · Nairobi · 14 Jun 2026' },
                  { dot:'green',  label:'Processed',          val:'EcoRecycle Kenya · Mechanical Recycling' },
                  { dot:'orange', label:'Upcycled By',        val:'Galant Branding International' },
                  { dot:'green',  label:'Blockchain Verified', val:'1.2 RECO minted · Stellar Network' },
                ].map((item,i,arr) => (
                  <React.Fragment key={i}>
                    <div className="story-step">
                      <div className={`story-dot ${item.dot}`}/>
                      <div>
                        <p className="story-label">{item.label}</p>
                        <p className="story-val">{item.val}</p>
                      </div>
                    </div>
                    {i < arr.length - 1 && <div className="story-line"/>}
                  </React.Fragment>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* About Us */}
      <section id="about" className="section about-section">
        <div className="section-inner">
          <div className="section-header">
            <p className="section-tag">ABOUT US</p>
            <h2>Built for Kenya's Circular Economy</h2>
            <p className="section-sub">We exist to formalize, digitize, and verify Kenya's waste sector — creating a system where every kilogram counts.</p>
          </div>
          <div className="about-grid">
            {[
              { color:'green',  icon:<LeafIcon size={22}/>,   title:'Our Mission',      body:'To create a transparent, inclusive system where every waste collector is recognized, every kilogram is counted, every payment is instant, and every impact is verified on the blockchain.' },
              { color:'orange', icon:<GlobeIcon size={22}/>,  title:'The Problem We Solve', body:'Millions of informal waste pickers work daily with no formal records, no reliable payment, and no proof of impact. Recyclers lack supply chain visibility. MatXchange changes that.' },
              { color:'green',  icon:<ChartIcon size={22}/>,  title:'Our Vision',       body:'A Kenya where every recycled product carries a verified story — from the hand that collected it to the shelf it sits on — and where circular economy data drives real investment and policy.' },
            ].map((c,i) => (
              <div className="about-card" key={i}>
                <div className={`about-icon ${c.color}`}>{c.icon}</div>
                <h3>{c.title}</h3>
                <p>{c.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="cta-section">
        <div className="cta-inner">
          <h2>Ready to join Kenya's circular economy?</h2>
          <p>Whether you're a waste collector, recycler, brand, or organization — there's a place for you on MatXchange.</p>
          <Link to="/login" className="btn-primary btn-large">Get Started <ArrowRight size={18}/></Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-inner">
          <div className="footer-brand">
            <img src={mx_logo} alt="MatXchange" className="footer-logo"/>
            <p>The digital backbone for Kenya's circular economy.</p>
          </div>
          <div className="footer-links">
            <div className="footer-col">
              <h4>Platform</h4>
              <button onClick={() => scrollTo('how-it-works')}>How It Works</button>
              <button onClick={() => scrollTo('solutions')}>Solutions</button>
              <button onClick={() => scrollTo('qr')}>QR Passports</button>
            </div>
            <div className="footer-col">
              <h4>Company</h4>
              <button onClick={() => scrollTo('about')}>About Us</button>
              <button onClick={() => scrollTo('home')}>Impact</button>
            </div>
            <div className="footer-col">
              <h4>Get Started</h4>
              <Link to="/login">Log In</Link>
              <Link to="/login">Sign Up</Link>
            </div>
          </div>
        </div>
        <div className="footer-bottom">
          <p>© 2026 MatXchange. All rights reserved. Built for Kenya's circular economy.</p>
        </div>
      </footer>
    </div>
  )
}

export default LandingPage