import hashlib,html.parser,json,os,pathlib,subprocess,tempfile,unittest,zipfile,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
ENGINE_NAME='hexbazaar_savage_intel_shop_v0_1_2_rc1.py'
class P(html.parser.HTMLParser):
 def __init__(self):
  super().__init__();self.ids=set();self.buttons=[];self.local_links=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  if tag=='button' and 'data-copy' in a:self.buttons.append(a['data-copy'])
  if tag in ('a','img','script','link'):
   for key in ('href','src'):
    if a.get(key) and not a[key].startswith(('https://','http://','#','mailto:')):self.local_links.append(a[key])
class Tests(unittest.TestCase):
 def test_page_links_and_copy_ids(self):
  totals=0
  for name in ('index.html','commands.html','providers.html','help.html'):
   parser=P();parser.feed((ROOT/name).read_text())
   self.assertTrue(parser.buttons,name)
   for ref in parser.local_links:self.assertTrue((ROOT/ref).is_file(),f'{name}: {ref}')
   for bid in parser.buttons:self.assertIn(bid,parser.ids)
   totals+=len(parser.buttons)
  self.assertGreaterEqual(totals,10)
 def test_art_matches_existing_approved_source(self):
  # Hash pinned to the owned original v0.1.2 package, not fabricated new art.
  self.assertEqual(hashlib.sha256((ROOT/'assets/rosie-hexbazaar-approved.png').read_bytes()).hexdigest(),
   '2ecc5dbc21e875e531d1aa7af8645393a5fde8fe2fa48bb40c5e05be197ee208')
 def test_launch_preserves_default_no_demo(self):
  s=(ROOT/'RUN_HEXBAZAAR_LIVE.sh').read_text()
  self.assertIn('--live --providers dns',s)
  self.assertIn('--live --providers dns,ripe,certspotter,urlscan',s)
  self.assertNotIn(' --color always demo',s)
 def test_installed_engine_invocation(self):
  with tempfile.TemporaryDirectory() as home:
   d=pathlib.Path(home)/'PhantomLabsLaunchers/hexbazaar-savage-intel-shop-v0_1_2_rc1_rosie_savage'
   d.mkdir(parents=True)
   p=d/ENGINE_NAME
   p.write_text('import sys,json,os\nopen(os.environ["LOGFILE"],"w").write(json.dumps(sys.argv[1:]))\n')
   env={**os.environ,'HOME':home,'LOGFILE':str(pathlib.Path(home)/'cmd.json')}
   for mode,domain,providers in [('start','example.com','dns'),('easy','facebook.com','dns'),('medium','example.com','dns,ripe'),('savage','facebook.com','dns,ripe,certspotter,urlscan')]:
    r=subprocess.run(['bash',str(ROOT/'RUN_HEXBAZAAR_LIVE.sh'),mode],env=env,capture_output=True,text=True)
    self.assertEqual(r.returncode,0,r.stderr)
    args=json.loads((pathlib.Path(home)/'cmd.json').read_text())
    self.assertIn('--live',args)
    self.assertEqual(args[args.index('domain')+1],domain)
    self.assertEqual(args[args.index('--providers')+1],providers)
 def test_missing_engine_reports_failure(self):
  with tempfile.TemporaryDirectory() as home:
   r=subprocess.run(['bash',str(ROOT/'RUN_HEXBAZAAR_LIVE.sh'),'easy'],env={**os.environ,'HOME':home},capture_output=True,text=True)
   self.assertEqual(r.returncode,3);self.assertIn('not found',r.stderr)
 def test_installer_preserves_existing_alias_and_icon(self):
  with tempfile.TemporaryDirectory() as home:
   base=pathlib.Path(home);alias=base/'.local/bin/hexbazaar-live-deck';alias.parent.mkdir(parents=True)
   alias.write_text('existing command');icon=base/'Desktop/HEXBAZAAR-Live-Command-Deck-v1.desktop';icon.parent.mkdir(parents=True);icon.write_text('existing desktop icon')
   env={**os.environ,'HOME':home,'PATH':'/usr/bin:/bin'}
   r=subprocess.run(['bash',str(ROOT/'INSTALL_DESKTOP_AND_ALIAS.sh')],env=env,capture_output=True,text=True)
   self.assertEqual(r.returncode,0,r.stderr)
   self.assertEqual(alias.read_text(),'existing command');self.assertEqual(icon.read_text(),'existing desktop icon')
 def test_installer_creates_short_alias(self):
  with tempfile.TemporaryDirectory() as home:
   env={**os.environ,'HOME':home,'PATH':'/usr/bin:/bin'}
   r=subprocess.run(['bash',str(ROOT/'INSTALL_DESKTOP_AND_ALIAS.sh')],env=env,capture_output=True,text=True)
   self.assertEqual(r.returncode,0,r.stderr)
   alias=pathlib.Path(home)/'.local/bin/hexbazaar-live-deck';self.assertTrue(alias.is_file())
   r=subprocess.run([str(alias),'help'],env=env,capture_output=True,text=True)
   self.assertEqual(r.returncode,0,r.stderr);self.assertIn('SAVAGE',r.stdout.upper())
if __name__=='__main__':unittest.main()
