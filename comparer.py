from coldtype import *
from subprocess import run
from git import Repo

def run_fontmake(sha, ufo_path, directory="compiled"):
    ufo_folder = __FILE__.parent / directory
    ufo_folder.mkdir(exist_ok=True, parents=True)
    
    fontmade_path = ufo_folder / f"{sha}.otf"
    fontmade_path.parent.mkdir(exist_ok=True)
    
    run([
        "fontmake",
        "-u", str(ufo_path),
        "-o", "otf",
        "--output-path=" + str(fontmade_path)], capture_output=True)
    
    return fontmade_path

folder = Path("~/Type/typewest").expanduser()
repo = Repo(str(folder))

#repo.git.checkout("main")
commits = list(repo.iter_commits('main', max_count=200))
shas = [(c.hexsha, c.committed_date) for c in commits]

for sha, date in shas[49:100]:
    repo.git.checkout(sha)
    print("checkedout", sha)
    ufo = folder / "clarendons/ufos/chars_manual.ufo"
    ufo2 = folder / "clarendons/ufos/chars.ufo"
    if ufo.exists():
        print("running", sha)
        path = run_fontmake(str(date), ufo)
        print(path)
    elif ufo2.exists():
        print("running2", sha)
        path = run_fontmake(str(date), ufo2)
        print(path)
    else:
        print("no chars")
    repo.git.checkout("main")
    print("checkedout main")

@renderable()
def stub(r):
    return (DATPen()
        .oval(r.inset(50))
        .f(0.8))
